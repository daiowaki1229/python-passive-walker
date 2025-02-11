#!/usr/bin/env python3

# dynamical_system.py
# Copyright (c) 2025 Dai Owaki <owaki@tohoku.ac.jp>
# ver. 2025.2.2.

import numpy as np

# 制御入力を返す関数（現在は制御なし）
def controlinput(x):
    return 0.0

# 二重振り子の運動方程式を定義する関数（ODE用）
def DoublePendulum(t, p, params):
    
    # パラメータの設定
    alpha = params[0]            # 斜面の角度
    beta  = params[2] / params[1] # 振り脚と股関節の質量比
    gamma = params[4] / params[3] # 重力加速度 / 脚の長さ
    
    # 状態変数を展開
    theta_st  = p[0]  # 支持脚の角度
    dtheta_st = p[1]  # 支持脚の角速度
    theta_sw  = p[2]  # 振り脚の角度
    dtheta_sw = p[3]  # 振り脚の角速度
    
    # 制御入力（現在はゼロ）
    F = controlinput(p)
    
    # 質量行列の定義
    M = np.matrix([[1 + 2 * beta * (1 - np.cos(theta_sw)), -beta * (1 - np.cos(theta_sw))],
                   [-beta * (1 - np.cos(theta_sw)), beta]])
    
    # 運動項の行列
    N = np.matrix([[-beta * np.sin(theta_sw) * (dtheta_sw * dtheta_sw - 2 * dtheta_st * dtheta_sw)],
                   [-beta * dtheta_st * dtheta_st * np.sin(theta_sw)]])
    
    # 重力項の行列
    G = np.matrix([[beta * gamma * (np.sin(theta_st - theta_sw - alpha) - np.sin(theta_st - alpha)) - gamma * np.sin(theta_st - alpha)],
                   [-beta * gamma * np.sin(theta_st - theta_sw - alpha)]])
    
    # 逆行列を求めて加速度を計算
    IM = np.linalg.inv(M)    
    A = (-1) * IM.dot(N + G)
    
    # 計算結果をスカラー値に変換
    ddtheta_st = A[0, 0].item()
    ddtheta_sw = A[1, 0].item()
    
    # 角速度と角加速度を返す
    return np.array([dtheta_st, ddtheta_st, dtheta_sw, ddtheta_sw])

# 歩行の遷移ルールを定義する関数
def TransitionRule(p, params):
    
    # パラメータの設定
    alpha = params[0]            # 斜面の角度
    beta  = params[2] / params[1] # 振り脚と股関節の質量比
    gamma = params[4] / params[3] # 重力加速度 / 脚の長さ

    # 幾何学的条件を設定
    theta_st  = -p[0]   # 支持脚の角度を反転
    theta_sw  = -2 * p[0]  # 振り脚の角度を反転
    
    # 遷移時の角速度の計算
    dtheta_st = (np.cos(p[2]) / (1 + beta * np.sin(p[2]) * np.sin(p[2]))) * p[1]
    dtheta_sw = ((np.cos(p[2]) * (1 - np.cos(p[2]))) / (1 + beta * np.sin(p[2]) * np.sin(p[2]))) * p[1]
    
    # 更新された状態を返す
    return np.array([theta_st, dtheta_st, theta_sw, dtheta_sw])
