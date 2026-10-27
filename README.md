# バドミントン ポール表示シミュレーション

RVizでコート、ロボット、ネット、2本のポールと模式カメラ画像を表示します。幾何学描画のためGazebo、物理演算、実写画像、Florence認識、自己位置推定、ロボットの移動制御は含みません。対象はROS 2 Foxy、Ubuntu 20.04、Python 3.8です。Jetsonでは同じFoxy環境で実行できます。ROS 2 / RViz の実起動は作成環境では未検証です。

## 導入

```bash
sudo apt install ros-foxy-rviz2 python3-opencv python3-numpy python3-colcon-common-extensions
mkdir -p ~/badminton_ws/src
# この badminton_poles_sim ディレクトリを ~/badminton_ws/src/ にコピー
cd ~/badminton_ws
source /opt/ros/foxy/setup.bash
colcon build --packages-select badminton_poles_sim
source install/setup.bash
ros2 launch badminton_poles_sim demo.launch.py
```

RVizの「2D Pose Estimate」を選択し、コート上でドラッグするとロボット位置と向きを変更できます。回転させない場合は毎回同じ方向にドラッグしてください。青い箱がロボット、オレンジの矢印が前方です。Image欄にカメラ画像を表示します。見えない場合はDisplaysのCamera Imageを展開してImage Topicを `/sim_camera/image_raw` に設定してください。

座標はmapで、ポールは (0, +3.05), (0, -3.05) m、ロボット初期位置は (-4, 0) m、向き0 rad（+X）です。ネットは表示用で実際の形状や遮蔽は再現していません。画像は歪みなしピンホールの簡易描画で、太さや遮蔽を正確には再現しません。カメラはロボット中心上にあります。

パラメータを変更する場合は別ターミナルから実行します（設定は再起動後には戻ります）。

```bash
ros2 param set /badminton_poles_sim pole_spacing 5.0
ros2 param set /badminton_poles_sim hfov_deg 110.0
```

`robot_x`, `robot_y`, `robot_yaw` は起動時の値です。位置を変更するにはRVizの2D Pose Estimateを使用してください。その他 `pole_height`, `camera_height` を変更できます。`/sim_camera/camera_info` を出力しますが、光学フレームのTFは配信していません。

## Foxy版の変更点

- RVizの各DisplayにEnabled/Valueを明示し、起動時に表示が有効になるように設定。
- 2D Pose EstimateのTopicを文字列形式で設定。
- launchとament_index_pythonの実行依存を追加。
- Python 3.8文法互換性、XML/YAMLの静的検証を実施。

既存の同名パッケージがある場合はソースをこの版へ置き換え、ワークスペースで再ビルドしてください。同時に複数の版を起動しないでください。

JetsonにSSHで接続する場合、RVizは画面を表示できる環境で起動してください。描画ノードだけを起動するには以下を使用できます。

```bash
ros2 run badminton_poles_sim sim
```

## 動作確認

```bash
ros2 topic hz /sim_camera/image_raw
ros2 topic echo /sim_camera/camera_info --once
```

ポールが見えない場合はロボットが+X方向を向き、両方のポールが画角に入る位置にあることを確認してください。初期状態で左右に2本表示されます。カメラ画像内のネットは未描画です。
