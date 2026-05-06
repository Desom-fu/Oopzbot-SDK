# Message Service

`Message Service` 用于发送频道消息、发送私信、打开私信会话、撤回消息、获取频道历史消息和置顶消息。

---

## `open_private_session(target)`

打开或创建与指定用户的私信会话。

```python
session = await client.messages.open_private_session(target="用户 UID")
print(session.session_id)
```

=== "参数"

    | 参数 | 类型 | 必填 | 说明 |
    | --- | --- | --- | --- |
    | `target` | `str` | 是 | 目标用户 UID，不能为空。 |

=== "返回值"

    返回：`PrivateSession`。

    对应模型：`oopz_sdk.models.PrivateSession`

    | 字段 | 类型 | 默认值 | API 字段 | 说明 |
    | --- | --- | --- | --- | --- |
    | `uid` | `str` | `""` | `uid` | 对方用户 UID。 |
    | `last_time` | `str` | `""` | `lastTime` | 会话最后更新时间。 |
    | `mute` | `bool` | `False` | `mute` | 当前私信会话是否静音。 |
    | `session_id` | `str` | `""` | `sessionId` | 私信会话 ID。发送私信或撤回私信时会用到。 |

---

## `send_message(*texts, area, channel, ...)`

发送频道消息。

```python
result = await client.messages.send_message(
    "hello",
    area="域 ID",
    channel="频道 ID",
)

print(result.message_id)
```

=== "参数"

    | 参数 | 类型 | 必填 | 默认值 | 说明 |
    | --- | --- | --- | --- | --- |
    | `*texts` | `str \| Segment` | 是 | - | 文本或 Segment 列表。多个参数会被合并为一条消息 |
    | `area` | `str` | 是 | - | 域 ID，不能为空 |
    | `channel` | `str` | 是 | - | 频道 ID，不能为空 |
    | `attachments` | `list \| None` | 否 | `None` | 手动附件列表；不能与 Segment 方式混用 |
    | `mention_list` | `list \| None` | 否 | `None` | 手动 mention 列表 |
    | `is_mention_all` | `bool` | 否 | `False` | 是否at全体 |
    | `style_tags` | `list \| None` | 否 | `None` | 样式标签，例如 `IMPORTANT` |
    | `reference_message_id` | `str \| None` | 否 | `None` | 被回复消息 ID |
    | `animated` | `bool` | 否 | `False` |  |
    | `display_name` | `str` | 否 | `""` | 展示名 |
    | `duration` | `int` | 否 | `0` | 媒体时长 |
    | `version` | `"v1" \| "v2"` | 否 | `"v2"` | 发送接口版本 |

=== "返回值"

    返回：`MessageSendResult`。

    对应模型：`oopz_sdk.models.MessageSendResult`

    | 字段 | 类型 | 默认值 | API 字段 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | 无 | `messageId` | Oopz 消息 ID。撤回、置顶、回复时通常会用到。 |
    | `timestamp` | `str` | `""` | `timestamp` | 消息时间戳。 |

=== "Segment 示例"

    ```python
    from oopz_sdk.models.segment import Text, Image

    result = await bot.messages.send_message(
        Text("图片：\n"),
        Image("./a.png"),
        area=area,
        channel=channel,
    )

    print(result.message_id)
    ```

=== "说明"

    `send_message()` 会先把 `str` 或 `Segment` 统一处理成 Oopz 消息内容。

    如果传入的是普通字符串：

    ```python
    await bot.messages.send_message(
        "hello",
        area=area,
        channel=channel,
    )
    ```

    SDK 会直接发送文本消息。

    如果传入的是 `Image` 这类 Segment，SDK 会先读取并上传图片输入，再生成 Oopz 需要的图片占位文本和附件信息。图片输入支持本地路径、bytes、base64 / data URL 和 file-like 对象，详见 [Media Service](media-service.md)。

---

## `send_private_message(*texts, target, channel=None, ...)`

发送私信。

如果没有传入 `channel`，SDK 会先调用 `open_private_session(target)` 打开或创建私信会话，然后再发送消息。

```python
result = await client.messages.send_private_message(
    "你好",
    target="用户 UID",
)

print(result.message_id)
```

=== "参数"

    | 参数 | 类型 | 必填 | 默认值 | 说明 |
    | --- | --- | --- | --- | --- |
    | `*texts` | `str \| Segment` | 是 | - | 文本或 Segment 列表。 |
    | `target` | `str` | 是 | - | 目标用户 UID，不能为空。 |
    | `channel` | `str \| None` | 否 | `None` | 私信会话 ID；不传时自动调用 `open_private_session()`。 |
    | `attachments` | `list \| None` | 否 | `None` | 手动附件列表；不能与 Segment 方式混用。 |
    | `mention_list` | `list \| None` | 否 | `None` | 手动 mention 列表。 |
    | `is_mention_all` | `bool` | 否 | `False` | 是否at全体。 |
    | `style_tags` | `list \| None` | 否 | `None` | 样式标签。 |
    | `reference_message_id` | `str \| None` | 否 | `None` | 被回复消息 ID。 |
    | `animated` | `bool` | 否 | `False` | 附件动画标记。 |
    | `display_name` | `str` | 否 | `""` | 展示名。 |
    | `duration` | `int` | 否 | `0` | 媒体时长。 |
    | `version` | `"v1" \| "v2"` | 否 | `"v2"` | 发送接口版本。 |

=== "返回值"

    返回：`MessageSendResult`。

    对应模型：`oopz_sdk.models.MessageSendResult`

    | 字段 | 类型 | 默认值 | API 字段 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | 无 | `messageId` | Oopz 消息 ID。 |
    | `timestamp` | `str` | `""` | `timestamp` | 消息时间戳。 |

=== "指定私信会话"

    如果你已经通过 `open_private_session()` 获取过私信会话 ID，可以直接传入 `channel`。

    ```python
    session = await client.messages.open_private_session(target="用户 UID")

    result = await client.messages.send_private_message(
        "你好",
        target="用户 UID",
        channel=session.session_id,
    )
    ```

---

## `recall_message(message_id, area, channel, timestamp=None, target="")`

撤回频道消息。

```python
result = await client.messages.recall_message(
    message_id,
    area=area,
    channel=channel,
)

print(result.ok)
```

=== "参数"

    | 参数 | 类型 | 必填 | 默认值 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | 是 | - | Oopz 消息 ID，不能为空。 |
    | `area` | `str` | 是 | - | 域 ID，不能为空。 |
    | `channel` | `str` | 是 | - | 频道 ID，不能为空。 |
    | `timestamp` | `str \| int \| float \| None` | 否 | `None` | 可选时间戳；不传时 SDK 自动生成当前微秒时间戳。 |
    | `target` | `str` | 否 | `""` | 可选目标。频道消息此处应留空。 |

=== "返回值"

    返回：`OperationResult`。

    对应模型：`oopz_sdk.models.OperationResult`

    | 字段 | 类型 | 默认值 | 说明 |
    | --- | --- | --- | --- |
    | `ok` | `bool` | `True` | 操作是否成功。 |
    | `message` | `str` | `""` | 操作消息或错误信息。 |

=== "说明"

    频道消息撤回需要同时知道：

    - `message_id`
    - `area`
    - `channel`

---

## `recall_private_message(message_id, channel, target, area=None, timestamp=None)`

撤回私信消息。

私信撤回需要私信会话 `channel` 与目标用户 `target`。

```python
result = await client.messages.recall_private_message(
    message_id,
    channel="私信会话 ID",
    target="用户 UID",
)

print(result.ok)
```

=== "参数"

    | 参数 | 类型 | 必填 | 默认值 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | 是 | - | Oopz 消息 ID，不能为空。 |
    | `channel` | `str` | 是 | - | 私信会话 ID，不能为空。 |
    | `target` | `str` | 是 | - | 目标用户 UID，不能为空。(See `open_private_session()`) |
    | `area` | `str \| None` | 否 | `None` | 私信目标所属域 ID。一般可不传。 |
    | `timestamp` | `str \| int \| float \| None` | 否 | `None` | 可选时间戳；不传时 SDK 自动生成当前微秒时间戳。 |

=== "返回值"

    返回：`OperationResult`。

    对应模型：`oopz_sdk.models.OperationResult`

    | 字段 | 类型 | 默认值 | 说明 |
    | --- | --- | --- | --- |
    | `ok` | `bool` | `True` | 操作是否成功。 |
    | `message` | `str` | `""` | 操作消息或错误信息。 |

---

## `get_channel_messages(area, channel, size=50)`

获取频道历史消息。

```python
messages = await client.messages.get_channel_messages(
    area=area,
    channel=channel,
)

for message in messages:
    print(message.message_id, message.text)
```

=== "参数"

    | 参数 | 类型 | 必填 | 默认值 | 说明 |
    | --- | --- | --- | --- | --- |
    | `area` | `str` | 是 | - | 域 ID，不能为空。 |
    | `channel` | `str` | 是 | - | 频道 ID，不能为空。 |
    | `size` | `int` | 否 | `50` | 拉取条数，必须为正整数。 |

=== "返回值"

    返回：`list[Message]`。

    对应模型：`oopz_sdk.models.Message`

    | 字段 | 类型 | 默认值 | API 字段 | 说明 |
    | --- | --- | --- | --- | --- |
    | `target` | `str` | `""` | `target` | 目标用户或目标对象。 |
    | `area` | `str` | `""` | `area` | 域 ID。 |
    | `area_page` | `str` | `""` | `areaPage` | 域分页或页面信息。 |
    | `area_count` | `int` | `0` | `areaCount` | 域相关计数。 |
    | `channel` | `str` | `""` | `channel` | 频道 ID。 |
    | `message_type` | `str` | `""` | `type` | 消息类型，例如文本、图片等。 |
    | `client_message_id` | `str` | `""` | `clientMessageId` | 客户端消息 ID。 |
    | `message_id` | `str` | `""` | `messageId` | Oopz 消息 ID。 |
    | `timestamp` | `str` | `""` | `timestamp` | 消息时间戳。 |
    | `sender_id` | `str` | `""` | `person` | 发送者 UID。 |
    | `content` | `str` | `""` | `content` | 原始消息内容。 |
    | `text` | `str` | `""` | `text` | 文本内容。 |
    | `edit_time` | `int` | `0` | `editTime` | 编辑时间。 |
    | `top_time` | `str` | `""` | `topTime` | 置顶时间。 |
    | `duration` | `int` | `0` | `duration` | 媒体时长。 |
    | `display_name` | `str` | `""` | `displayName` | 展示名。 |
    | `preview_image` | `MediaInfo \| None` | `None` | `previewImage` | 预览图信息。 |
    | `raw_video` | `MediaInfo \| None` | `None` | `rawVideo` | 原始视频信息。 |
    | `cards` | `Any` | `None` | `cards` | 卡片数据。 |
    | `mention_list` | `list[MentionInfo]` | `[]` | `mentionList` | at列表。 |
    | `is_mention_all` | `bool` | `False` | `isMentionAll` | 是否at全体。 |
    | `sender_is_bot` | `bool` | `False` | `senderIsBot` | 发送者是否为机器人。 |
    | `sender_bot_type` | `str` | `""` | `senderBotType` | 发送者机器人类型。 |
    | `style_tags` | `list[Any]` | `[]` | `styleTags` | 样式标签。 |
    | `reference_message` | `Any` | `None` | `referenceMessage` | 被引用消息对象。 |
    | `reference_message_id` | `str` | `""` | `referenceMessageId` | 被引用消息 ID。 |
    | `attachments` | `list[Attachment]` | `[]` | `attachments` | 附件列表。 |

=== "说明"

    `get_channel_messages()` 会把接口返回的消息项转换成 `Message` 模型。

    如果你只是想监听实时消息，通常不需要主动调用这个方法。监听消息可以使用：

    ```python
    @bot.on_message
    async def handle_message(message, ctx):
        print(message.text)
    ```

---

## `top_message(message_id, channel, area, top_message=True)`

置顶或取消置顶频道消息。

```python
await client.messages.top_message(
    message_id,
    channel=channel,
    area=area,
    top_message=True,
)

await client.messages.top_message(
    message_id,
    channel=channel,
    area=area,
    top_message=False,
)
```

=== "参数"

    | 参数 | 类型 | 必填 | 默认值 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | 是 | - | Oopz 消息 ID，不能为空。 |
    | `channel` | `str` | 是 | - | 频道 ID，不能为空。 |
    | `area` | `str` | 是 | - | 域 ID，不能为空。 |
    | `top_message` | `bool` | 否 | `True` | `True` 表示置顶，`False` 表示取消置顶。 |

=== "返回值"

    返回：`OperationResult`。

    对应模型：`oopz_sdk.models.OperationResult`

    | 字段 | 类型 | 默认值 | 说明 |
    | --- | --- | --- | --- |
    | `ok` | `bool` | `True` | 操作是否成功。 |
    | `message` | `str` | `""` | 操作消息或错误信息。 |

---

## Segment 发送建议

使用 `Image` 时 SDK 会：

1. 读取图片输入、宽高和文件大小。
2. 上传图片数据。
3. 生成 Oopz 图片占位文本 `![IMAGEw{width}h{height}]({file_key})`。
4. 生成附件列表。
5. 与send_message()的其他文本参数合并成完整消息内容。

=== "示例"

    ```python
    from oopz_sdk.models.segment import Text, Image

    await bot.messages.send_message(
        Text("图片：\n"),
        Image("./a.png"),
        area=area,
        channel=channel,
    )
    ```

=== "为什么推荐 Segment"

    Segment 方式更适合 SDK 用户，因为它可以隐藏底层 Oopz 消息格式。

    例如图片消息底层需要同时处理：

    - 图片占位文本
    - 附件列表
    - 图片宽高
    - 文件上传结果

    使用 `Image` 时，这些步骤会由 SDK 自动完成。

=== "注意事项"

    同时使用Segment 和手动 `attachments`是不被允许的，因为这会导致消息内容和附件列表不一致，SDK 无法正确处理。

    例如下面这种写法应该避免：

    ```python
    await bot.messages.send_message(
        Image.from_file("./a.png"),
        attachments=[...],
        area=area,
        channel=channel,
    )
    ```

    因为 SDK 无法明确判断附件应该来自 Segment 还是手动参数。

---

## `get_channel_message_reactions(message_id)`

获取单条频道消息的全部表情回应汇总。

```python
item = await client.messages.get_channel_message_reactions(
    message_id="消息 ID",
)

print(item.message_id)

for emoji in item.emojis:
    print(emoji.emoji, emoji.person_count, emoji.me)
```

=== "参数"

    | 参数 | 类型 | 必填 | 说明 |
    | --- | --- | --- | --- |
    | `message_id` | `str` | 是 | Oopz 消息 ID，不能为空。 |

=== "返回值"

    返回：`MessageEmojiItem`。

    对应模型：`oopz_sdk.models.MessageEmojiItem`

    | 字段 | 类型 | 默认值 | API 字段 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | `""` | `messageId` | Oopz 消息 ID。 |
    | `emojis` | `list[MessageEmoji]` | `[]` | `emojis` | 该消息上的表情回应列表。 |

    `MessageEmoji` 字段：

    | 字段 | 类型 | 默认值 | API 字段 | 说明 |
    | --- | --- | --- | --- | --- |
    | `emoji` | `str` | `""` | `emoji` | 表情内容。 |
    | `person_count` | `int` | `0` | `personCount` | 回应该表情的人数。 |
    | `me` | `bool` | `False` | `me` | 当前账号是否回应了该表情。 |
    | `created_at` | `str` | `""` | `createdAt` | 表情回应创建时间。通常是微秒时间戳字符串。 |

=== "说明"

    该方法会调用频道消息 reaction 汇总接口，并将返回项转换为 `MessageEmojiItem`。

    如果接口返回的列表数量不是 `1`，SDK 会抛出异常，因为单条消息查询预期只返回一条消息的 reaction 汇总。

---

## `get_channel_message_reactions_batch(message_ids)`

批量获取频道消息的表情回应汇总。

```python
items = await client.messages.get_channel_message_reactions_batch(
    [
        "消息 ID 1",
        "消息 ID 2",
    ]
)

for item in items:
    print(item.message_id, item.emojis)
```

=== "参数"

    | 参数 | 类型 | 必填 | 说明 |
    | --- | --- | --- | --- |
    | `message_ids` | `list[str]` | 是 | Oopz 消息 ID 列表。数量必须大于 `0`，且不能超过 `50`。 |

=== "返回值"

    返回：`list[MessageEmojiItem]`。

    对应模型：`oopz_sdk.models.MessageEmojiItem`

    | 字段 | 类型 | 默认值 | API 字段 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | `""` | `messageId` | Oopz 消息 ID。 |
    | `emojis` | `list[MessageEmoji]` | `[]` | `emojis` | 该消息上的表情回应列表。 |

=== "注意"

    单次批量查询最多支持 `50` 条消息。

---

## `get_private_message_reactions(message_id)`

获取单条私信消息的全部表情回应汇总。

```python
item = await client.messages.get_private_message_reactions(
    message_id="消息 ID",
)

print(item.message_id)

for emoji in item.emojis:
    print(emoji.emoji, emoji.person_count, emoji.me)
```

=== "参数"

    | 参数 | 类型 | 必填 | 说明 |
    | --- | --- | --- | --- |
    | `message_id` | `str` | 是 | Oopz 消息 ID，不能为空。 |

=== "返回值"

    返回：`MessageEmojiItem`。

    对应模型：`oopz_sdk.models.MessageEmojiItem`

    | 字段 | 类型 | 默认值 | API 字段 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | `""` | `messageId` | Oopz 消息 ID。 |
    | `emojis` | `list[MessageEmoji]` | `[]` | `emojis` | 该消息上的表情回应列表。 |

    `MessageEmoji` 字段：

    | 字段 | 类型 | 默认值 | API 字段 | 说明 |
    | --- | --- | --- | --- | --- |
    | `emoji` | `str` | `""` | `emoji` | 表情内容。 |
    | `person_count` | `int` | `0` | `personCount` | 回应该表情的人数。 |
    | `me` | `bool` | `False` | `me` | 当前账号是否回应了该表情。 |
    | `created_at` | `str` | `""` | `createdAt` | 表情回应创建时间。通常是微秒时间戳字符串。 |

=== "说明"

    该方法会调用私信消息 reaction 汇总接口，并将返回项转换为 `MessageEmojiItem`。

    如果接口返回的列表数量不是 `1`，SDK 会抛出异常，因为单条消息查询预期只返回一条消息的 reaction 汇总。

---

## `get_private_message_reactions_batch(message_ids)`

批量获取私信消息的表情回应汇总。

```python
items = await client.messages.get_private_message_reactions_batch(
    [
        "消息 ID 1",
        "消息 ID 2",
    ]
)

for item in items:
    print(item.message_id, item.emojis)
```

=== "参数"

    | 参数 | 类型 | 必填 | 说明 |
    | --- | --- | --- | --- |
    | `message_ids` | `list[str]` | 是 | Oopz 消息 ID 列表。数量必须大于 `0`，且不能超过 `50`。 |

=== "返回值"

    返回：`list[MessageEmojiItem]`。

    对应模型：`oopz_sdk.models.MessageEmojiItem`

    | 字段 | 类型 | 默认值 | API 字段 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | `""` | `messageId` | Oopz 消息 ID。 |
    | `emojis` | `list[MessageEmoji]` | `[]` | `emojis` | 该消息上的表情回应列表。 |

=== "注意"

    单次批量查询最多支持 `50` 条消息。

---

## `add_channel_reaction(message_id, area, channel, emoji)`

给频道消息添加表情回应。

```python
result = await client.messages.add_channel_reaction(
    message_id="消息 ID",
    area="域 ID",
    channel="频道 ID",
    emoji="❤️",
)

print(result.ok)
```

=== "参数"

    | 参数 | 类型 | 必填 | 说明 |
    | --- | --- | --- | --- |
    | `message_id` | `str` | 是 | Oopz 消息 ID，不能为空。 |
    | `area` | `str` | 是 | 域 ID，不能为空。 |
    | `channel` | `str` | 是 | 频道 ID，不能为空。 |
    | `emoji` | `str` | 是 | 表情回应，支持真实 emoji、十进制 Unicode 或十六进制 Unicode。 |

=== "返回值"

    返回：`OperationResult`。

    对应模型：`oopz_sdk.models.OperationResult`

    | 字段 | 类型 | 默认值 | 说明 |
    | --- | --- | --- | --- |
    | `ok` | `bool` | `True` | 操作是否成功。 |
    | `message` | `str` | `""` | 操作消息或错误信息。 |

=== "说明"

    表情参数 `emoji` 支持：

    - 真实 emoji，例如 `❤️`
    - 十进制 Unicode，例如 `10084`
    - 十六进制 Unicode，例如 `0x2764`

    ```python
    await client.messages.add_channel_reaction(message_id, area=area, channel=channel, emoji="❤️")
    await client.messages.add_channel_reaction(message_id, area=area, channel=channel, emoji="10084")
    await client.messages.add_channel_reaction(message_id, area=area, channel=channel, emoji="0x2764")
    ```

    支持列表见下文 [reaction-emoji-支持列表](#reaction-emoji-支持列表)。 使用了不支持的表情会导致sdk返回ValueError异常。

---

## `add_private_reaction(message_id, channel, target, emoji, area="")`

给私信消息添加表情回应。

```python
result = await client.messages.add_private_reaction(
    message_id="消息 ID",
    channel="私信会话 ID",
    target="用户 UID",
    emoji="❤️",
)

print(result.ok)
```

=== "参数"

    | 参数 | 类型 | 必填 | 默认值 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | 是 | - | Oopz 消息 ID，不能为空。 |
    | `channel` | `str` | 是 | - | 私信会话 ID，不能为空。 |
    | `target` | `str` | 是 | - | 目标用户 UID，不能为空。 |
    | `emoji` | `str` | 是 | - | 表情回应，支持真实 emoji、十进制 Unicode 或十六进制 Unicode。 |
    | `area` | `str` | 否 | `""` | 私信目标所属域 ID。一般可不传。 |

=== "返回值"

    返回：`OperationResult`。

    对应模型：`oopz_sdk.models.OperationResult`

    | 字段 | 类型 | 默认值 | 说明 |
    | --- | --- | --- | --- |
    | `ok` | `bool` | `True` | 操作是否成功。 |
    | `message` | `str` | `""` | 操作消息或错误信息。 |

=== "说明"

    表情参数 `emoji` 支持：

    - 真实 emoji，例如 `❤️`
    - 十进制 Unicode，例如 `10084`
    - 十六进制 Unicode，例如 `0x2764`

    支持列表见下文 [reaction-emoji-支持列表](#reaction-emoji-支持列表) 。使用了不支持的表情会导致sdk返回ValueError异常。

---

## `get_channel_reaction_persons(message_id, channel, emoji, page=1, page_size=4)`

获取频道消息中回应了指定表情的用户列表。

```python
uids = await client.messages.get_channel_reaction_persons(
    message_id="消息 ID",
    channel="频道 ID",
    emoji="❤️",
)

for uid in uids:
    print(uid)
```

=== "参数"

    | 参数 | 类型 | 必填 | 默认值 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | 是 | - | Oopz 消息 ID，不能为空。 |
    | `channel` | `str` | 是 | - | 频道 ID，不能为空。 |
    | `emoji` | `str` | 是 | - | 要查询的[表情](#reaction-emoji-支持列表)，支持真实 emoji、十进制 Unicode 或十六进制 Unicode。 |
    | `page` | `int` | 否 | `1` | 页码。 |
    | `page_size` | `int` | 否 | `4` | 每页数量。 |

=== "返回值"

    返回：`list[str]`。

    列表中的每一项是回应了该表情的用户 UID。

=== "说明"

    这个方法只查询某一个指定表情的回应用户。

    如果想先获取某条消息包含哪些表情回应，可以使用 `get_channel_message_reactions()`。

---

## `get_private_reaction_persons(message_id, channel, emoji, page=1, page_size=4)`

获取私信消息中回应了指定表情的用户列表。

```python
uids = await client.messages.get_private_reaction_persons(
    message_id="消息 ID",
    channel="私信会话 ID",
    emoji="❤️",
)

for uid in uids:
    print(uid)
```

=== "参数"

    | 参数 | 类型 | 必填 | 默认值 | 说明 |
    | --- | --- | --- | --- | --- |
    | `message_id` | `str` | 是 | - | Oopz 消息 ID，不能为空。 |
    | `channel` | `str` | 是 | - | 私信会话 ID，不能为空。 |
    | `emoji` | `str` | 是 | - | 要查询的[表情](#reaction-emoji-支持列表)，支持真实 emoji、十进制 Unicode 或十六进制 Unicode。 |
    | `page` | `int` | 否 | `1` | 页码。 |
    | `page_size` | `int` | 否 | `4` | 每页数量。 |

=== "返回值"

    返回：`list[str]`。

    列表中的每一项是回应了该表情的用户 UID。

---

## Reaction Emoji 支持列表

| Emoji | Unicode   | 中文      | Emoji | Unicode  | 中文           |
|------:|-----------|:--------|------:|----------|:-------------|
|       | `1061376` | 无语      |    😰 | `128560` | 冷汗           |
|       | `1061377` | 皱眉看手机   |    😥 | `128549` | 失望但如释重负      |
|       | `1061378` | 黑人问号    |    😓 | `128531` | 汗            |
|       | `1061379` | 爱心脸     |    🤗 | `129303` | 抱抱           |
|       | `1061380` | 捂嘴哭     |    🤔 | `129300` | 想一想          |
|       | `1061381` | 捂脸哭     |    🤭 | `129325` | 不说           |
|       | `1061382` | 苦笑      |    🥱 | `129393` | 打呵欠          |
|       | `1061383` | 笑喷      |    🤫 | `129323` | 安静的脸         |
|       | `1061384` | 捂嘴笑     |    🤥 | `129317` | 说谎           |
|       | `1061386` | 叹气      |    😐 | `128528` | 冷漠           |
|       | `1061387` | 无语流汗    |    😑 | `128529` | 无语           |
|       | `1061388` | 疑问      |    😬 | `128556` | 龇牙咧嘴         |
|       | `1061389` | 暗中观察    |    🙄 | `128580` | 翻白眼          |
|       | `1061390` | 捂脸      |    😯 | `128559` | 缄默           |
|       | `1061391` | 狗头      |    😦 | `128550` | 啊            |
|    😀 | `128512`  | 嘿嘿      |    😧 | `128551` | 极度痛苦         |
|    😃 | `128515`  | 哈哈      |    😲 | `128562` | 震惊           |
|    😄 | `128516`  | 大笑      |    😴 | `128564` | 睡着了          |
|    😁 | `128513`  | 嘻嘻      |    🤤 | `129316` | 流口水          |
|    😆 | `128518`  | 斜眼笑     |    😪 | `128554` | 困            |
|    😅 | `128517`  | 苦笑      |    😵 | `128565` | 晕头转向         |
|    😂 | `128514`  | 笑哭了     |    🤐 | `129296` | 闭嘴           |
|    🤣 | `129315`  | 笑得满地打滚  |    🥴 | `129396` | 头昏眼花         |
|    😊 | `128522`  | 羞涩微笑    |    🤢 | `129314` | 恶心           |
|     ☺ | `9786`    | 微笑      |    🤮 | `129326` | 呕吐           |
|    😇 | `128519`  | 微笑天使    |    🤧 | `129319` | 打喷嚏          |
|    🙂 | `128578`  | 呵呵      |    😷 | `128567` | 感冒           |
|    🙃 | `128579`  | 倒脸      |    🤒 | `129298` | 发烧           |
|    😉 | `128521`  | 眨眼      |    🤕 | `129301` | 受伤           |
|    😌 | `128524`  | 松了口气    |    🤑 | `129297` | 发财           |
|    🥲 | `129394`  | 含泪的笑脸   |    🤠 | `129312` | 牛仔帽脸         |
|    😍 | `128525`  | 花痴      |    🥸 | `129400` | 伪装的脸         |
|    🥰 | `129392`  | 喜笑颜开    |    😈 | `128520` | 恶魔微笑         |
|    😘 | `128536`  | 飞吻      |    👿 | `128127` | 生气的恶魔        |
|    😗 | `128535`  | 亲亲      |    👹 | `128121` | 食人魔          |
|    😙 | `128537`  | 微笑亲亲    |    👺 | `128122` | 小妖精          |
|    😚 | `128538`  | 羞涩亲亲    |    🤡 | `129313` | 小丑脸          |
|    😋 | `128523`  | 好吃      |    🫣 | `129763` | 偷看表情         |
|    😛 | `128539`  | 吐舌      |    🫢 | `129762` | 睁着眼睛、手捂住嘴的表情 |
|    😝 | `128541`  | 眯眼吐舌    |    🫡 | `129761` | 敬礼表情         |
|    😜 | `128540`  | 单眼吐舌    |    🫥 | `129765` | 虚线表情         |
|    🤪 | `129322`  | 滑稽      |    🥹 | `129401` | 强忍泪水表情       |
|    🤨 | `129320`  | 挑眉      |    🫤 | `129764` | 歪嘴表情         |
|    🧐 | `129488`  | 带单片眼镜的脸 |    🫠 | `129760` | 融化表情         |
|    🤓 | `129299`  | 书呆子脸    |    💩 | `128169` | 大便           |
|    😎 | `128526`  | 墨镜笑脸    |    💤 | `128164` | 睡着           |
|    🤩 | `129321`  | 好崇拜哦    |    💣 | `128163` | 炸弹           |
|    🥳 | `129395`  | 聚会笑脸    |    💢 | `128162` | 怒            |
|    😏 | `128527`  | 得意      |    💋 | `128139` | 唇印           |
|    😒 | `128530`  | 不高兴     |    🌹 | `127801` | 玫瑰           |
|    😞 | `128542`  | 失望      |    🥀 | `129344` | 枯萎的花         |
|    😔 | `128532`  | 沉思      |     ❤ | `10084`  | 红心           |
|    😟 | `128543`  | 担心      |    💔 | `128148` | 心碎           |
|    😕 | `128533`  | 困扰      |    👌 | `128076` | Ok           |
|    🙁 | `128577`  | 微微不满    |    🖐 | `128400` | 手掌           |
|     ☹ | `9785`    | 不满      |    🤌 | `129292` | 捏手指          |
|    😣 | `128547`  | 痛苦      |    🤏 | `129295` | 捏合的手势        |
|    😖 | `128534`  | 困惑      |     ✌ | `9996`   | 胜利手势         |
|    😫 | `128555`  | 累       |    🤞 | `129310` | 交叉的手指        |
|    😩 | `128553`  | 累死了     |    🫰 | `129776` | 食指和拇指交叉的手    |
|    🥺 | `129402`  | 恳求的脸    |    🤙 | `129305` | 给我打电话        |
|    😢 | `128546`  | 哭       |    👉 | `128073` | 反手食指向右指      |
|    😭 | `128557`  | 放声大哭    |    👈 | `128072` | 反手食指向左指      |
|    😤 | `128548`  | 傲慢      |    🫶 | `129782` | 心形手          |
|    😮 | `128558`  | 呼气      |    👆 | `128070` | 反手食指向上指      |
|    😠 | `128544`  | 生气      |    👇 | `128071` | 反手食指向下指      |
|    😡 | `128545`  | 怒火中烧    |    🫵 | `129781` | 食指指向观众       |
|    🤬 | `129324`  | 嘴上有符号的脸 |    👍 | `128077` | 拇指向上         |
|    🤯 | `129327`  | 爆炸头     |    👎 | `128078` | 拇指向下         |
|    😳 | `128563`  | 脸红      |     ✊ | `9994`   | 举起拳头         |
|    😶 | `128566`  | 迷茫      |    👏 | `128079` | 鼓掌           |
|    🥵 | `129397`  | 脸发烧     |    🤝 | `129309` | 握手           |
|    🥶 | `129398`  | 冷脸      |    🙏 | `128591` | 双手合十         |
|    😱 | `128561`  | 吓死了     |    💪 | `128170` | 肌肉           |
|    😨 | `128552`  | 害怕      |       |          |              |
