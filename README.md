# Passive Walker Simulation

This repository contains a simulation of a passive dynamic walker using Python. The simulation models the motion of a bipedal robot that walks down a slope under the influence of gravity without active control.

本リポジトリには、Pythonを用いた受動歩行シミュレーションが含まれています。本シミュレーションは、能動的な制御なしに、重力の影響だけで斜面を歩行する二足歩行ロボットの動作をモデル化しています。

## Features / 特徴
- Solves the equations of motion using ODE (Ordinary Differential Equation) integration.
- Provides real-time visualization of the walking motion.
- Includes a Streamlit web application for easy interaction.

- ODE（常微分方程式）を用いた運動方程式の解法。
- 歩行モーションのリアルタイム可視化。
- Streamlitを用いたWebアプリによる簡単な操作。

## Files / ファイル一覧

| File | Description |
|------|-------------|
| `passive_walker_ode.py` | Main program: sets parameters, initial conditions, runs the ODE simulation, and implements state transition rules. |
| `dynamical_system.py` | Library for dynamical system calculations. |
| `video_passive_walker.py` | Library for animation display. |
| `streamlit_passive_walker.py` | Streamlit-based web application for visualization. |

| ファイル名 | 説明 |
|------------|------|
| `passive_walker_ode.py` | メインプログラム：パラメータ・初期条件の設定、ODE計算の実行、状態遷移則の実装。 |
| `dynamical_system.py` | 力学計算用のライブラリ。 |
| `video_passive_walker.py` | アニメーション表示用のライブラリ。 |
| `streamlit_passive_walker.py` | Streamlitを用いたWebアプリの実行コード。 |

## Installation / インストール

Ensure you have Python installed (version 3.8 or later). Required libraries can be installed using:

Python 3.8以上がインストールされていることを確認してください。必要なライブラリは以下のコマンドでインストールできます。

```sh
pip install scipy numpy matplotlib
```

To run the Streamlit web application, install the following:

Streamlitを使用してWebアプリを実行する場合、以下のライブラリが必要です。

```sh
pip install streamlit
```

## Usage / 実行方法

### Run the Simulation / シミュレーションを実行

To run the simulation, execute the following command:

シミュレーションを実行するには、以下のコマンドを実行してください。

```sh
python passive_walker_ode.py
```

This will run the simulation, displaying key values in the terminal such as the stance phase duration and state variables (stance leg angle, swing leg angle, stance leg angular velocity, and swing leg angular velocity). Once completed, an animation of the walking motion will be displayed.

このコマンドを実行すると、各接地タイミングごとの1周期の時間や、状態変数（支持脚角度、遊脚角度、支持脚角速度、遊脚角速度）がターミナルに表示され、シミュレーションが完了するとアニメーションが表示されます。

### Run the Web Application / Webアプリを実行

To launch the Streamlit web application, run:

StreamlitによるWebアプリを起動するには、以下のコマンドを実行してください。

```sh
streamlit run streamlit_passive_walker.py
```

This will open a browser window displaying the walking animation interactively.

これにより、ブラウザで歩行アニメーションをインタラクティブに表示できます。

### Try the Web Application Online / Webアプリをオンラインで試す

You can access the web application via Streamlit Cloud:

Streamlit CloudでWebアプリを試すことができます。

[Passive Walker Web App](https://python-passive-walker.streamlit.app)

## License / ライセンス
This project is licensed under the MIT License.

本プロジェクトはMITライセンスの下で公開されています。

## Acknowledgments / 謝辞
This project is inspired by passive dynamic walking studies and serves as an educational tool for understanding bipedal locomotion dynamics.

本プロジェクトは受動歩行に関する研究から着想を得ており、二足歩行の力学を理解するための教育ツールとして活用できます。

## References / 参考文献
- Tad McGeer. Passive dynamic walking. The International Journal of Robotics Research, 9:62–82, 1990.
- Mariano Garcia, Anindya Chatterjee, Andy Ruina, and Michael J. Coleman. The simplest walking model: stability, complexity, and scaling. Journal of biomechanical engineering, 120 2:281–8, 1998.
- Ambarish Goswami, Benoit Thuilot, and Bernard Espiau. Compass-like biped robot part i : Stability and bifurcation of passive gaits. 1996.
- Dai Owaki, Koichi Osuka, and Akio Ishiguro. On the embodiment that enables passive dynamic bipedal running. 2008 IEEE International Conference on Robotics and Automation, pages 341–346, 2008.
- Dai Owaki, Koichi Osuka, and Akio Ishiguro. Stabilization mechanism underlying passive dynamic running. Advanced Robotics, 27:1399–1407, 2013.


---
Feel free to contribute or report any issues!

貢献や問題報告を歓迎します！

