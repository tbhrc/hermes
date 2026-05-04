# Media Delivery Reference
## send_message Tool Behavior
### Supported MEDIA Platforms
Direct MEDIA delivery (attaching files via `MEDIA:/path`) is only supported for:
- telegram
- discord
- matrix
- weixin
- signal
- yuanbao

### WhatsApp Workaround
Direct `send_message` to `whatsapp:*` targets fails for MEDIA. To deliver media to the user's WhatsApp:
1. Send to Telegram home channel: `target=telegram:2053906913` (user's configured home channel ID).
2. The send response will include `mirrored: true`, confirming auto-forward to the user's linked WhatsApp DM.

### Verification
- Check send response for `mirrored: true` to confirm WhatsApp delivery.
- Direct WhatsApp send error: "MEDIA delivery is currently only supported for telegram, discord, matrix, weixin, signal and yuanbao"
- Supported platforms verified in this session: Telegram sends with MEDIA work, direct WhatsApp MEDIA fails.