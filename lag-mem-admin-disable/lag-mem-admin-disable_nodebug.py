# 必要なライブラリをインポートする
import sys
import json

# イベントハンドラのメインエントリ関数
def event_handler_main(in_json_str):
    # イベントハンドラから渡された入力JSON文字列を解析する
    in_json = json.loads(in_json_str)
    # JSONから"paths"と"options"を取得する
    paths = in_json["paths"]
    options = in_json["options"]

    # 応答アクションを格納するリスト
    response_actions = []
    # LAGメンバーを格納する辞書
    lag_members = {}

    # pathsを反復処理する
    for path in paths:
        # pathをスペースで分割してリストにする
        path_parts = path["path"].split(" ")

        # pathに"lag member"が含まれている場合、lag_members辞書に追加する
        if "lag member" in path["path"]:
            # インターフェース名を取得する
            interface = path_parts[1]
            # インターフェースが辞書に存在しない場合、新しいリストを作成する
            if interface not in lag_members:
                lag_members[interface] = []
            # メンバーをインターフェースのリストに追加する
            lag_members[interface].append(path_parts[4])

    # pathsを再度反復処理する
    for path in paths:
        # pathをスペースで分割してリストにする
        path_parts = path["path"].split(" ")

        # pathに"admin-state"が含まれている場合、管理状態を確認し、オペレーション状態を設定する
        if "admin-state" in path["path"]:
            # インターフェース名を取得する
            interface = path_parts[1]
            # 管理状態を取得する
            admin_state = path["value"]
            # インターフェースがlag_membersに存在する場合
            if interface in lag_members:
                # 各メンバーに対して処理を行う
                for member in lag_members[interface]:
                    # 管理状態が"disable"の場合、メンバーのオペレーション状態を"down"に設定する
                    if admin_state == "disable":
                        response_actions.append(
                            {
                                "set-ephemeral-path": {
                                    "path": f"interface {member} oper-state",
                                    "value": "down",
                                }
                            }
                        )
                    # 管理状態が"enable"の場合、メンバーのオペレーション状態を"up"に設定する
                    elif admin_state == "enable":
                        response_actions.append(
                            {
                                "set-ephemeral-path": {
                                    "path": f"interface {member} oper-state",
                                    "value": "up",
                                }
                            }
                        )

    # 応答を辞書形式で作成し、JSON文字列として返す
    response = {"actions": response_actions}
    return json.dumps(response)

# メイン関数を実行し、その後スクリプトを終了する
if __name__ == "__main__":
    sys.exit(main())















