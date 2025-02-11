#!/usr/bin/env python3

# passive_walker_ode.py
# Copyright (c) 2025 Dai Owaki <owaki@tohoku.ac.jp>
# ver. 2025.2.2.

# 必要なライブラリをインポート
from scipy.integrate import odeint
from scipy.integrate import ode
import numpy as np

# 自作モジュールのインポート
import dynamical_system as ds
import video_passive_walker as v

# シミュレーションのパラメータ設定
m_hip = 1.0          # 股関節の質量 [kg]
m_sw  = 0.050        # 振り脚の質量 [kg]
l     = 0.50         # 脚の長さ [m]
g     = 9.8          # 重力加速度 [m/s^2]
alpha = -0.00050 * np.pi  # 斜面の角度 [rad]

beta  = m_sw / m_hip  # 質量比
gamma = g / l         # 周波数 (二乗される)

params = [alpha, m_hip, m_sw, l, g]  # シミュレーションパラメータ

# 初期条件の設定
max_t = 10.0  # シミュレーションの最大時間 [s]
dt = 0.00010  # 時間ステップ [s]
times = 100   # 動画のスピード倍率

video_dt = dt * times


def run_simulation(max_t, dt, params, times):
    
    # 初期状態ベクトル (角度と角速度)
    x0 = np.array([-0.10791001, 0.52174036, -0.21582003, 0.01216315])
    #m_sw = 0.05, alpha = -0.00050*np.pi
    
    # 状態変数と時間の配列を準備
    x = np.empty([int(max_t/dt), 4])
    t = np.empty([int(max_t/dt)])
    t[0] = 0.0

    # ODE ソルバーの設定
    solver = ode(ds.DoublePendulum).set_integrator('vode', method='bdf')
    #solver = ode(ds.DoublePendulum).set_integrator('dopri5')
    #solver = ode(ds.DoublePendulum).set_integrator('dop853')
    solver.set_f_params((params))
    solver.set_initial_value(x0, 0.0)
    
    x[0] = x0  # 初期状態を格納

    # シミュレーションフラグ
    Transition = False  # 遷移フラグ
    Fall = False        # 転倒フラグ
    TimeLimit = False   # 時間制限フラグ
    i = 0
    step = 0
    tmp_t = 0.0

    # 足の座標を記録する配列
    foot = np.empty([int(max_t/dt)+1, 2])
    foot[0, 0] = 0.0  # x座標
    foot[0, 1] = 0.0  # y座標

    # シミュレーションループ
    while TimeLimit == False and Fall == False:
        while solver.successful() and Transition == False and solver.t < (max_t - dt) and Fall == False:
            solver.integrate(solver.t + dt)
            t[i] = solver.t
            x[i] = solver.y
            i += 1
            foot[i, :] = foot[i-1, :]
            
            # 遷移条件の判定
            if (solver.y[0]) > 0.010:
                if 0.000 < (2 * solver.y[0] - solver.y[2]) < 0.010:
                    Transition = True
                    step += 1
                    x0 = ds.TransitionRule(x[i-1, :], params)
                    print(solver.t - tmp_t, x0)
                    tmp_t = solver.t
                    
                    # 足の位置を更新
                    foot[i, 0] += params[3] * np.sin(x[i-1, 0] - params[0]) - params[3] * np.sin(x[i-1, 0] - x[i-1, 2] - params[0])
                    foot[i, 1] += params[3] * np.cos(x[i-1, 0] - params[0]) - params[3] * np.cos(x[i-1, 0] - x[i-1, 2] - params[0])
            
            # 転倒条件の判定
            if np.tan(params[0]) * (params[3] * np.sin(solver.y[0] - params[0])) > params[3] * np.cos(solver.y[0] - params[0]):
                Fall = True

        # 次の初期条件を設定
        solver.set_initial_value(x0, t[i-1])
        Transition = False

        if t[i-1] > max_t - 2 * dt:
            TimeLimit = True

    # 動画用のデータを作成
    
    length = min(len(x), len(foot))  # x と foot の最小サイズを取得
    indices = np.arange(0, length, times)  # 安全な範囲でインデックスを生成
    video_x = x[indices]
    video_foot = foot[indices]        

    # 動画を生成（通常速度）
    # v.video(x, dt, max_t, params, foot)
    
    return video_x, video_foot
    





if __name__ == '__main__':

    video_x, video_foot = run_simulation(max_t, dt, params, times)

    # 動画を高速再生
    v.video(video_x, video_dt, max_t, params, video_foot)
