
# streamlit_passive_walker.py
# Copyright (c) 2025 Dai Owaki <owaki@tohoku.ac.jp>
# ver. 2025.2.2.

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
from passive_walker_ode import run_simulation

# Streamlit アプリの設定
st.title("Passive Walker Simulation")

# 初期条件の設定
#max_t = 10.0  # シミュレーションの最大時間 [s]
dt = 0.00010  # 時間ステップ [s]

# シミュレーションパラメータの設定
max_t = float(st.sidebar.number_input("Simulation Time (s)", min_value=5.0, max_value=30.0, value=10.0, step=5.0, format="%.1f"))
times = int(st.sidebar.number_input("Animation Speed Multiplier", min_value=100.0, max_value=1000.0, value=100.0, step=100.0, format="%.1f"))
alpha = float(st.sidebar.number_input("Slope Angle (rad)", min_value=0.0000, max_value=0.0100, value=0.0005, step=0.0001, format="%.5f"))


video_dt = dt * times

# セッションステートの初期化
if "run_simulation" not in st.session_state:
    st.session_state.run_simulation = False
if "stop_simulation" not in st.session_state:
    st.session_state.stop_simulation = False

# シミュレーションの実行制御
if st.button("Run Simulation"):
    st.session_state.run_simulation = True
    st.session_state.stop_simulation = False

if st.button("Stop Simulation"):
    st.session_state.run_simulation = False
    st.session_state.stop_simulation = True

if st.session_state.run_simulation:
    with st.spinner("Running Simulation..."):
        
        params = [alpha * (-np.pi), 1.0, 0.050, 0.50, 9.8]  # 固定パラメータ
        x, foot = run_simulation(max_t, dt, params, times)

        # プロット用の空のコンテナ
        plot_area = st.empty()
        
        # アニメーションの設定
        #fig, ax = plt.subplots()
        # 図の初期設定
        fig = plt.figure(figsize=(6, 9))
        gs  = gridspec.GridSpec(2, 1)
        
        # フォントの設定をTimes New Romanに変更
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 20  # フォントサイズを20に設定
        
        # ax1エリアの設定
        ax1 = fig.add_subplot(gs[0, 0], xlim=(-0.40, 0.40), ylim=(-0.2, 0.6))
        ax1.set_xlabel('x [m]')
        ax1.set_ylabel('y [m]')
        ax1.grid()
        
        slope, = ax1.plot([], [], 'k-', lw=1)            # 斜面        
        stleg, = ax1.plot([], [], 'b-', lw=3)  # 支持脚
        swleg, = ax1.plot([], [], 'b-', lw=3)  # 振り脚
        hip,   = ax1.plot([], [], 'mo', markersize=20)  # 股関節
        knee,  = ax1.plot([], [], 'co', markersize=10)  # 膝
        foot_p, = ax1.plot([], [], 'ro', markersize=10)  # 足の描画

        # 時間のリストを作成
        time_seq  = np.arange(0.0, max_t, video_dt)

        # アニメーション用のテキストテンプレートを設定
        time_template = 'time = %.3f s'
        time_text = ax1.text(0.05, 0.925, '', transform=ax1.transAxes)
        
        theta_st_template = 'theta(st) = %.3f rad'
        theta_st_text = ax1.text(0.05, 0.15, '', transform=ax1.transAxes)
        theta_sw_template = 'theta(sw) = %.3f rad'
        theta_sw_text = ax1.text(0.05, 0.05, '', transform=ax1.transAxes)
        
        
        # ax2エリアの設定
        ax2 = fig.add_subplot(gs[1, 0], xlim=(-0.5, 0.5), ylim=(-0.5, 2.0))
        ax2.set_xlabel('theta(st) [rad]')
        ax2.set_ylabel('dtheta(st) [rad]')
        ax2.grid()

        # 軌道をプロット
        cycle_st, = plt.plot(x[:, 0], x[:, 1], 'm-', lw=1.5, alpha=0.2)  # 支持脚の軌道
        cycle_sw, = plt.plot(x[:, 2], x[:, 3], 'c-', lw=1.5, alpha=0.2)  # 遊脚の軌道

        pt_st, = plt.plot([], [], 'mo', markersize=10, alpha=1.0)  # 支持脚のポイント
        pt_sw, = plt.plot([], [], 'co', markersize=10, alpha=1.0)  # 遊脚のポイント

        plt.tight_layout()
        
        for i in range(len(x)):
            if st.session_state.stop_simulation:
                break
        
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
            
            time_text.set_text(time_template % time_seq[i])          # 時間テキストの表示
            theta_st_text.set_text(theta_st_template % (x[i,0])) # 支持脚角度の表示
            theta_sw_text.set_text(theta_sw_template % (x[i,2])) # 遊脚角度の表示
                        
            pt_st.set_data([x[i,0]], [x[i,1]]) # 支持脚軌道の設定
            pt_sw.set_data([x[i,2]], [x[i,3]]) # 遊脚軌道の設定
            
            plot_area.pyplot(fig)  # Streamlit上でプロットを更新
            time.sleep(video_dt)  # フレーム更新間隔
