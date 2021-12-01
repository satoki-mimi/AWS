# minecraft-discord-aws-lambda

## 概要
DiscordのApplication Commandsを使用して、Amazon EC2インスタンス（Minecraftサーバ）を起動もしくは停止する。
以下のWebサイトを参考に（ほぼコピペで）作成しました。

## 参考
- https://oozio.medium.com/serverless-discord-bot-55f95f26f743
- https://github.com/oozio/discord_aws_bot_demo

## その他
- PyNaClライブラリを設定する際に、Amazon Linux 2でpip installしたものをレイヤーにインポートしましたがエラーとなったため、
ローカルPC（Ubuntu 20.04）でインストールしたものをレイヤーにインポートしました。
- 参考にしたWebサイトでは、Interaction Typeが4となっていますが、仕様が変わったので3にする必要があります。
https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
