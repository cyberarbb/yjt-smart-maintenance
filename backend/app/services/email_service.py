"""
이메일 발송 서비스
- SMTP를 통한 HTML 이메일 발송
- 네임카드 서명 자동 삽입
- 문의 답변 이메일 발송
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_settings
from app.models.user import User

logger = logging.getLogger(__name__)
settings = get_settings()


def build_namecard_html(user: User) -> str:
    """사용자 네임카드 정보로 HTML 이메일 서명 생성"""
    # 커스텀 HTML이 있으면 우선 사용
    if user.namecard_custom_html and user.namecard_custom_html.strip():
        return user.namecard_custom_html

    # 네임카드 정보가 하나도 없으면 기본 서명
    has_namecard = any([
        user.namecard_title, user.namecard_department,
        user.namecard_mobile, user.namecard_fax,
        user.namecard_address, user.namecard_website,
    ])

    if not has_namecard:
        return f"""
        <div style="margin-top:24px; padding-top:16px; border-top:2px solid #2563eb;">
            <p style="margin:0; font-weight:600; color:#1e293b; font-size:14px;">{user.full_name}</p>
            <p style="margin:2px 0 0; color:#64748b; font-size:12px;">{user.company}</p>
            <p style="margin:8px 0 0; color:#64748b; font-size:12px;">
                Email: {user.email}{f' | Tel: {user.phone}' if user.phone else ''}
            </p>
        </div>
        """

    # 네임카드 정보로 전문적인 서명 생성
    lines = []
    lines.append(f'<p style="margin:0; font-weight:700; color:#1e293b; font-size:15px;">{user.full_name}</p>')

    if user.namecard_title or user.namecard_department:
        title_dept = " | ".join(filter(None, [user.namecard_title, user.namecard_department]))
        lines.append(f'<p style="margin:2px 0 0; color:#2563eb; font-size:12px; font-weight:500;">{title_dept}</p>')

    if user.company:
        lines.append(f'<p style="margin:2px 0 0; color:#475569; font-size:13px; font-weight:600;">{user.company}</p>')

    # 연락처 정보
    contact_lines = []
    if user.phone:
        contact_lines.append(f"Tel: {user.phone}")
    if user.namecard_mobile:
        contact_lines.append(f"Mobile: {user.namecard_mobile}")
    if user.namecard_fax:
        contact_lines.append(f"Fax: {user.namecard_fax}")
    if contact_lines:
        lines.append(f'<p style="margin:6px 0 0; color:#64748b; font-size:12px;">{" | ".join(contact_lines)}</p>')

    lines.append(f'<p style="margin:2px 0 0; color:#64748b; font-size:12px;">Email: {user.email}</p>')

    if user.namecard_address:
        lines.append(f'<p style="margin:2px 0 0; color:#64748b; font-size:12px;">{user.namecard_address}</p>')

    if user.namecard_website:
        lines.append(f'<p style="margin:2px 0 0;"><a href="{user.namecard_website}" style="color:#2563eb; font-size:12px; text-decoration:none;">{user.namecard_website}</a></p>')

    return f"""
    <div style="margin-top:24px; padding-top:16px; border-top:2px solid #2563eb;">
        {''.join(lines)}
    </div>
    """


def send_email(
    to_email: str,
    subject: str,
    body_html: str,
    sender_user: User | None = None,
    reply_to: str | None = None,
) -> dict:
    """
    HTML 이메일 발송
    - sender_user가 있으면 네임카드 서명 자동 삽입
    - SMTP 설정이 없으면 로그만 남기고 성공 반환 (개발 환경)
    """
    if not settings.smtp_user or not settings.smtp_password:
        logger.warning(f"[EMAIL-DEV] SMTP 미설정. To: {to_email}, Subject: {subject}")
        logger.info(f"[EMAIL-DEV] Body preview: {body_html[:200]}...")
        return {"success": True, "message": "Email logged (SMTP not configured)"}

    try:
        # 네임카드 서명 삽입
        signature_html = ""
        if sender_user:
            signature_html = build_namecard_html(sender_user)

        # 전체 HTML 이메일 구성
        full_html = f"""
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #1e293b; line-height: 1.6; max-width: 600px; margin: 0 auto;">
            <div style="padding: 20px 0;">
                {body_html}
            </div>
            {signature_html}
            <div style="margin-top:20px; padding-top:12px; border-top:1px solid #e2e8f0;">
                <p style="margin:0; color:#94a3b8; font-size:10px;">
                    Sent via YJT Smart Maintenance Platform | YONGJIN TURBO CO., LTD.
                </p>
            </div>
        </body>
        </html>
        """

        # MIME 메시지 생성
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        from_display = f"{sender_user.full_name} <{settings.smtp_user}>" if sender_user else f"{settings.smtp_from_name} <{settings.smtp_user}>"
        msg["From"] = from_display
        msg["To"] = to_email
        if reply_to:
            msg["Reply-To"] = reply_to
        elif sender_user:
            msg["Reply-To"] = sender_user.email

        msg.attach(MIMEText(full_html, "html", "utf-8"))

        # SMTP 발송
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)

        logger.info(f"[EMAIL] Sent to {to_email}: {subject}")
        return {"success": True, "message": f"Email sent to {to_email}"}

    except smtplib.SMTPAuthenticationError:
        logger.error("[EMAIL] SMTP authentication failed - check smtp_user/smtp_password")
        return {"success": False, "message": "SMTP authentication failed. Check email credentials."}
    except Exception as e:
        logger.error(f"[EMAIL] Failed to send: {e}")
        return {"success": False, "message": str(e)}


def send_inquiry_response_email(
    to_email: str,
    subject: str,
    original_message: str,
    response_text: str,
    sender_user: User | None = None,
    language: str = "en",
) -> dict:
    """문의 답변 이메일 발송 (원본 메시지 포함)"""
    # 언어별 레이블
    labels = {
        "ko": {"greeting": "안녕하세요", "original": "원본 문의", "response": "답변", "footer": "추가 문의사항이 있으시면 언제든 연락해 주세요."},
        "en": {"greeting": "Hello", "original": "Original Inquiry", "response": "Response", "footer": "If you have any further questions, please don't hesitate to contact us."},
        "zh": {"greeting": "您好", "original": "原始咨询", "response": "回复", "footer": "如有任何其他问题，请随时与我们联系。"},
        "ja": {"greeting": "お世話になっております", "original": "お問い合わせ内容", "response": "回答", "footer": "ご不明な点がございましたら、お気軽にお問い合わせください。"},
        "ar": {"greeting": "مرحبًا", "original": "الاستفسار الأصلي", "response": "الرد", "footer": "إذا كان لديك أي أسئلة إضافية، لا تتردد في الاتصال بنا."},
        "es": {"greeting": "Hola", "original": "Consulta original", "response": "Respuesta", "footer": "Si tiene alguna pregunta adicional, no dude en contactarnos."},
        "hi": {"greeting": "नमस्ते", "original": "मूल पूछताछ", "response": "उत्तर", "footer": "यदि आपके कोई और प्रश्न हैं, तो कृपया संपर्क करने में संकोच न करें।"},
        "fr": {"greeting": "Bonjour", "original": "Demande originale", "response": "Réponse", "footer": "Si vous avez d'autres questions, n'hésitez pas à nous contacter."},
    }
    l = labels.get(language, labels["en"])

    body_html = f"""
    <p style="margin:0 0 16px; font-size:14px;">{l['greeting']},</p>

    <div style="background:#eff6ff; border-left:4px solid #2563eb; padding:12px 16px; border-radius:0 8px 8px 0; margin-bottom:16px;">
        <p style="margin:0 0 4px; font-size:11px; color:#2563eb; font-weight:600; text-transform:uppercase;">{l['response']}</p>
        <p style="margin:0; font-size:14px; color:#1e293b; white-space:pre-wrap;">{response_text}</p>
    </div>

    <div style="background:#f8fafc; padding:12px 16px; border-radius:8px; margin-bottom:16px;">
        <p style="margin:0 0 4px; font-size:11px; color:#94a3b8; font-weight:600; text-transform:uppercase;">{l['original']}: {subject}</p>
        <p style="margin:0; font-size:13px; color:#64748b; white-space:pre-wrap;">{original_message}</p>
    </div>

    <p style="margin:0; font-size:13px; color:#64748b;">{l['footer']}</p>
    """

    return send_email(
        to_email=to_email,
        subject=f"Re: {subject}",
        body_html=body_html,
        sender_user=sender_user,
    )


def send_password_reset_email(to_email: str, code: str, language: str = "en") -> dict:
    """비밀번호 리셋 인증 코드 이메일 발송"""
    labels = {
        "ko": {"subject": "비밀번호 재설정 인증 코드", "greeting": "안녕하세요,", "message": "비밀번호 재설정을 위한 인증 코드입니다.", "code_label": "인증 코드", "expiry": "이 코드는 10분 후에 만료됩니다.", "ignore": "비밀번호 재설정을 요청하지 않으셨다면 이 이메일을 무시하세요."},
        "en": {"subject": "Password Reset Verification Code", "greeting": "Hello,", "message": "Here is your verification code to reset your password.", "code_label": "Verification Code", "expiry": "This code will expire in 10 minutes.", "ignore": "If you did not request a password reset, please ignore this email."},
        "zh": {"subject": "密码重置验证码", "greeting": "您好，", "message": "以下是您重置密码的验证码。", "code_label": "验证码", "expiry": "此验证码将在10分钟后过期。", "ignore": "如果您没有请求重置密码，请忽略此邮件。"},
        "ja": {"subject": "パスワードリセット認証コード", "greeting": "こんにちは、", "message": "パスワードリセットの認証コードです。", "code_label": "認証コード", "expiry": "このコードは10分後に期限切れになります。", "ignore": "パスワードリセットを要求していない場合は、このメールを無視してください。"},
        "ar": {"subject": "رمز التحقق لإعادة تعيين كلمة المرور", "greeting": "مرحبًا،", "message": "إليك رمز التحقق لإعادة تعيين كلمة المرور.", "code_label": "رمز التحقق", "expiry": "سينتهي هذا الرمز خلال 10 دقائق.", "ignore": "إذا لم تطلب إعادة تعيين كلمة المرور، يرجى تجاهل هذا البريد."},
        "es": {"subject": "Código de verificación para restablecer contraseña", "greeting": "Hola,", "message": "Aquí está su código de verificación para restablecer su contraseña.", "code_label": "Código de verificación", "expiry": "Este código expirará en 10 minutos.", "ignore": "Si no solicitó restablecer su contraseña, ignore este correo."},
        "hi": {"subject": "पासवर्ड रीसेट सत्यापन कोड", "greeting": "नमस्ते,", "message": "पासवर्ड रीसेट के लिए आपका सत्यापन कोड यहाँ है।", "code_label": "सत्यापन कोड", "expiry": "यह कोड 10 मिनट में समाप्त हो जाएगा।", "ignore": "यदि आपने पासवर्ड रीसेट का अनुरोध नहीं किया है, तो कृपया इस ईमेल को अनदेखा करें।"},
        "fr": {"subject": "Code de vérification pour la réinitialisation du mot de passe", "greeting": "Bonjour,", "message": "Voici votre code de vérification pour réinitialiser votre mot de passe.", "code_label": "Code de vérification", "expiry": "Ce code expirera dans 10 minutes.", "ignore": "Si vous n'avez pas demandé la réinitialisation de votre mot de passe, veuillez ignorer cet e-mail."},
    }
    l = labels.get(language, labels["en"])

    body_html = f"""
    <p style="margin:0 0 16px; font-size:14px;">{l['greeting']}</p>
    <p style="margin:0 0 20px; font-size:14px; color:#475569;">{l['message']}</p>

    <div style="background:#eff6ff; border:2px solid #2563eb; border-radius:12px; padding:24px; text-align:center; margin-bottom:20px;">
        <p style="margin:0 0 8px; font-size:12px; color:#2563eb; font-weight:600; text-transform:uppercase; letter-spacing:1px;">{l['code_label']}</p>
        <p style="margin:0; font-size:36px; font-weight:700; color:#1e40af; letter-spacing:8px; font-family:monospace;">{code}</p>
    </div>

    <p style="margin:0 0 8px; font-size:13px; color:#64748b;">⏰ {l['expiry']}</p>
    <p style="margin:0; font-size:12px; color:#94a3b8;">{l['ignore']}</p>
    """

    return send_email(
        to_email=to_email,
        subject=f"🔐 {l['subject']}",
        body_html=body_html,
    )
