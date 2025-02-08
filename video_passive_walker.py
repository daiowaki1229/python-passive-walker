#!/usr/bin/env python3

# 必要なライブラリをインポート
import matplotlib.pyplot as plt
import math as m
import numpy as np
import matplotlib as mpl
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation

# アニメーションの描画を行う関数
def video(x, dt, max_t, params, foot):
    
    # 図の初期設定
    fig = plt.figure(figsize=(12, 5))
    gs  = gridspec.GridSpec(1, 2)
    
    # フォントの設定をTimes New Romanに変更
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 20  # フォントサイズを20に設定

    # ax1エリアの設定
    ax1 = fig.add_subplot(gs[0, 0], xlim=(-0.40, 0.40), ylim=(-0.2, 0.6))
    ax1.set_xlabel('x [m]')
    ax1.set_ylabel('y [m]')
    ax1.grid()

    # アニメーション用のプロットオブジェクトを作成
    foot_p,  = plt.plot([], [], 'ro', markersize=10)         # 足の描画
    stleg,   = plt.plot([], [], 'b-', lw=3)                  # 支持脚の描画
    swleg,   = plt.plot([], [], 'b-', lw=3)                  # 遊脚の描画
    hip,     = plt.plot([], [], 'mo', markersize=20)         # 股関節の描画
    knee,    = plt.plot([], [], 'co', markersize=10)         # 膝の描画
    slope,   = plt.plot([], [], 'k-', lw=1)                  # 斜面の描画

    # 時間のリストを作成
    time  = np.arange(0.0, max_t, dt)

    # アニメーション用のテキストテンプレートを設定
    time_template = 'time = %.3f s'
    time_text = ax1.text(0.05, 0.925, '', transform=ax1.transAxes)
    
    theta_st_template = 'theta(st) = %.3f rad'
    theta_st_text = ax1.text(0.05, 0.15, '', transform=ax1.transAxes)
    theta_sw_template = 'theta(sw) = %.3f rad'
    theta_sw_text = ax1.text(0.05, 0.05, '', transform=ax1.transAxes)

    # ax3エリアの設定
    ax3 = fig.add_subplot(gs[0, 1], xlim=(-0.5, 0.5), ylim=(-0.5, 2.0))
    ax3.set_xlabel('theta(st) [rad]')
    ax3.set_ylabel('dtheta(st) [rad]')
    ax3.grid()

    # 軌道をプロット
    cycle_st, = plt.plot(x[:, 0], x[:, 1], 'm-', lw=1.5, alpha=0.2)  # 支持脚の軌道
    cycle_sw, = plt.plot(x[:, 2], x[:, 3], 'c-', lw=1.5, alpha=0.2)  # 遊脚の軌道

    pt_st, = plt.plot([], [], 'mo', markersize=10, alpha=1.0)  # 支持脚のポイント
    pt_sw, = plt.plot([], [], 'co', markersize=10, alpha=1.0)  # 遊脚のポイント

    plt.tight_layout()

    # 初期化関数（アニメーション開始前の状態を定義）
    def init():
        return slope, stleg, swleg, hip, knee, foot_p, time_text, theta_st_text, theta_sw_text, cycle_st, cycle_sw, pt_st, pt_sw

    # フレームごとのアニメーション関数
    def anime(i):
        next_hx   = foot[i,0] + params[3]*np.sin(x[i,0]-params[0])       # 股関節のx座標
        next_hy   = foot[i,1] + params[3]*np.cos(x[i,0]-params[0])       # 股関節のy座標
        next_kx   = next_hx - params[3]*np.sin(x[i,0]-x[i,2]-params[0])  # 股関節のx座標
        next_ky   = next_hy - params[3]*np.cos(x[i,0]-x[i,2]-params[0])  # 股関節のy座標
        next_tlx   = [foot[i,0], next_hx]  # 足先（支持脚）のx座標
        next_tly   = [foot[i,1], next_hy]  # 足先（支持脚）のy座標
        next_wlx   = [next_hx, next_kx]    # 足先（支持脚）のx座標
        next_wly   = [next_hy, next_ky]    # 足先（支持脚）のx座標

        # 斜面のx, y座標
        slope_x = [0.50, -0.50]
        slope_y = [np.tan(params[0])*(0.35-foot[i,0]+next_hx)+foot[i,1], np.tan(params[0])*(-0.35-foot[i,0]+next_hx)+foot[i,1]]

        foot_p.set_data([foot[i,0]-next_hx], [foot[i,1]]) # 足先位置の設定
        stleg.set_data([next_tlx-next_hx], [next_tly])    # 支持脚位置の設定
        swleg.set_data([next_wlx-next_hx], [next_wly])    # 遊脚位置の設定
        hip.set_data([0], [next_hy])                      # 股関節位置の設定
        knee.set_data([next_kx-next_hx], [next_ky])       # 膝関節位置の設定

        slope.set_data([slope_x], [slope_y]) #斜面の設定

        pt_st.set_data([x[i,0]], [x[i,1]]) # 支持脚軌道の設定
        pt_sw.set_data([x[i,2]], [x[i,3]]) # 遊脚軌道の設定

        time_text.set_text(time_template % time[i])          # 時間テキストの表示
        theta_st_text.set_text(theta_st_template % (x[i,0])) # 支持脚角度の表示
        theta_sw_text.set_text(theta_sw_template % (x[i,2])) # 遊脚角度の表示

        return slope, stleg, swleg, hip, knee, foot_p, time_text, theta_st_text, theta_sw_text, cycle_st, cycle_sw, pt_st, pt_sw

    # アニメーションの実行
    ani = animation.FuncAnimation(fig, anime, np.arange(1, len(x)), interval=dt * 1.0e+4, blit=True, init_func=init)
    #ani.save('py_passive_walker3_v2.mp4', writer='ffmpeg')　#動画保存用

    
    # アニメーションの表示
    plt.show()


    
