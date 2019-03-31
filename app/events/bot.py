
"""
与群组聊天机器人交互的模块

通过 request 的 `Authorization` 字段中的 token 做权限验证。
因此程序应该使用 ssl！！！否则会很不安全。

---
赛文续传仍然需要 session，session 用 group_user_id 标识，存在 redis 里边，设个 expire 时间。
同时用 rq-scheduler 定时删除 session（要先于 expire），同时向群里发送过期时间.

--- 消息广播与 指定发送给特定的 namespace（定时任务）
可以将 socket 存到全局，
定时任务通过 socket.handler.server.clients.values() 获取到 client，
然后调用 client.ws.send() 发送消息（应该能够判断 client 的 namespace）
"""
import functools
import json
import logging
from flask import Blueprint, request, abort
from geventwebsocket import WebSocketError
from typing import Callable

from app.service.auth.bot import validate_bot_token
from app.service.messages import handle_update
from . import ws_prefix

logger = logging.getLogger(__name__)

bot_bp = Blueprint(r'bot', __name__, url_prefix=f'{ws_prefix}/bot')


def authenticated_only(func: Callable):
    """
    验证 WS 的 upgrade 请求是否带有有效的 token
    """
    @functools.wraps(func)
    def wrapper(socket):
        # websocket 是发生在 http 握手后的，而且是同一个 tcp 连接
        # 因此可以直接使用 request 获取握手阶段的请求信息
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Token ') and not auth.startswith('token '):
            abort(401, description="请求未带有认证字段：`Authorization`，或认证字段不正确！")  # Unauthorized

        token_given = auth[len('Token '):].strip()
        if not token_given:
            abort(401, description="请求未带有认证字段：`Authorization`，或认证字段不正确！")

        if not validate_bot_token(token_given):  # 验证 token
            abort(403, description="Token 不正确，禁止访问！")  # Forbidden

        return func(socket)

    return wrapper


@bot_bp.route('/')
@authenticated_only
def echo_socket(socket):
    """
    被动消息处理
    """
    while not socket.closed:
        try:
            message = socket.receive()
            logger.debug(f"收到消息: {message}")

            reply = handle_update(message)
            socket.send(json.dumps(reply))
        except WebSocketError as e:
            logger.info(f"ws 连接异常：{e}")



