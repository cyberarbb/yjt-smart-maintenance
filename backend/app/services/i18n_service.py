"""다국어(i18n) 서비스 - 8개 언어 지원
한국어(ko), 영어(en), 중국어(zh), 일본어(ja), 아랍어(ar), 스페인어(es), 힌디어(hi), 프랑스어(fr)
"""

SUPPORTED_LANGUAGES = {
    "ko": {"name": "한국어", "native": "한국어", "dir": "ltr"},
    "en": {"name": "English", "native": "English", "dir": "ltr"},
    "zh": {"name": "Chinese", "native": "中文", "dir": "ltr"},
    "ja": {"name": "Japanese", "native": "日本語", "dir": "ltr"},
    "ar": {"name": "Arabic", "native": "العربية", "dir": "rtl"},
    "es": {"name": "Spanish", "native": "Español", "dir": "ltr"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "dir": "ltr"},
    "fr": {"name": "French", "native": "Français", "dir": "ltr"},
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UI 번역 데이터
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRANSLATIONS = {
    # ── 공통 (Common) ──
    "app_title": {
        "ko": "YJT 스마트 정비 플랫폼",
        "en": "YJT Smart Maintenance Platform",
        "zh": "YJT 智能维护平台",
        "ja": "YJT スマート保守プラットフォーム",
        "ar": "منصة YJT للصيانة الذكية",
        "es": "Plataforma de Mantenimiento Inteligente YJT",
        "hi": "YJT स्मार्ट रखरखाव प्लेटफ़ॉर्म",
        "fr": "Plateforme de Maintenance Intelligente YJT",
    },
    "global_service": {
        "ko": "24/7 글로벌 서비스",
        "en": "24/7 Global Service",
        "zh": "24/7 全球服务",
        "ja": "24時間グローバルサービス",
        "ar": "خدمة عالمية على مدار الساعة",
        "es": "Servicio Global 24/7",
        "hi": "24/7 वैश्विक सेवा",
        "fr": "Service Mondial 24/7",
    },

    # ── 사이드바 (Sidebar Navigation) ──
    "nav_dashboard": {
        "ko": "대시보드", "en": "Dashboard", "zh": "仪表盘", "ja": "ダッシュボード",
        "ar": "لوحة التحكم", "es": "Panel", "hi": "डैशबोर्ड", "fr": "Tableau de bord",
    },
    "nav_inventory": {
        "ko": "부품 재고", "en": "Parts Inventory", "zh": "零件库存", "ja": "部品在庫",
        "ar": "مخزون القطع", "es": "Inventario de Piezas", "hi": "पार्ट्स इन्वेंटरी", "fr": "Inventaire des Pièces",
    },
    "nav_orders": {
        "ko": "서비스 주문", "en": "Service Orders", "zh": "服务订单", "ja": "サービス注文",
        "ar": "طلبات الخدمة", "es": "Órdenes de Servicio", "hi": "सेवा ऑर्डर", "fr": "Commandes de Service",
    },
    "nav_chatbot": {
        "ko": "AI 어시스턴트", "en": "AI Assistant", "zh": "AI 助手", "ja": "AIアシスタント",
        "ar": "مساعد الذكاء الاصطناعي", "es": "Asistente IA", "hi": "AI सहायक", "fr": "Assistant IA",
    },
    "nav_inquiries": {
        "ko": "고객 문의", "en": "Customer Inquiries", "zh": "客户咨询", "ja": "お客様お問い合わせ",
        "ar": "استفسارات العملاء", "es": "Consultas de Clientes", "hi": "ग्राहक पूछताछ", "fr": "Demandes Clients",
    },

    # ── 인증 (Auth) ──
    "login": {
        "ko": "로그인", "en": "Log In", "zh": "登录", "ja": "ログイン",
        "ar": "تسجيل الدخول", "es": "Iniciar Sesión", "hi": "लॉग इन", "fr": "Se Connecter",
    },
    "register": {
        "ko": "회원가입", "en": "Sign Up", "zh": "注册", "ja": "新規登録",
        "ar": "التسجيل", "es": "Registrarse", "hi": "साइन अप", "fr": "S'inscrire",
    },
    "email": {
        "ko": "이메일", "en": "Email", "zh": "电子邮箱", "ja": "メール",
        "ar": "البريد الإلكتروني", "es": "Correo electrónico", "hi": "ईमेल", "fr": "E-mail",
    },
    "password": {
        "ko": "비밀번호", "en": "Password", "zh": "密码", "ja": "パスワード",
        "ar": "كلمة المرور", "es": "Contraseña", "hi": "पासवर्ड", "fr": "Mot de passe",
    },
    "full_name": {
        "ko": "이름", "en": "Full Name", "zh": "姓名", "ja": "氏名",
        "ar": "الاسم الكامل", "es": "Nombre Completo", "hi": "पूरा नाम", "fr": "Nom Complet",
    },
    "company": {
        "ko": "회사명", "en": "Company", "zh": "公司", "ja": "会社名",
        "ar": "الشركة", "es": "Empresa", "hi": "कंपनी", "fr": "Entreprise",
    },
    "country": {
        "ko": "국가", "en": "Country", "zh": "国家", "ja": "国",
        "ar": "الدولة", "es": "País", "hi": "देश", "fr": "Pays",
    },
    "phone": {
        "ko": "전화번호", "en": "Phone", "zh": "电话", "ja": "電話番号",
        "ar": "الهاتف", "es": "Teléfono", "hi": "फ़ोन", "fr": "Téléphone",
    },
    "logout": {
        "ko": "로그아웃", "en": "Log Out", "zh": "退出", "ja": "ログアウト",
        "ar": "تسجيل الخروج", "es": "Cerrar Sesión", "hi": "लॉग आउट", "fr": "Se Déconnecter",
    },
    "no_account": {
        "ko": "계정이 없으신가요?", "en": "Don't have an account?", "zh": "没有账号？", "ja": "アカウントをお持ちでないですか？",
        "ar": "ليس لديك حساب؟", "es": "¿No tienes cuenta?", "hi": "खाता नहीं है?", "fr": "Pas de compte ?",
    },
    "have_account": {
        "ko": "이미 계정이 있으신가요?", "en": "Already have an account?", "zh": "已有账号？", "ja": "すでにアカウントをお持ちですか？",
        "ar": "لديك حساب بالفعل؟", "es": "¿Ya tienes cuenta?", "hi": "पहले से खाता है?", "fr": "Déjà un compte ?",
    },
    "welcome_back": {
        "ko": "돌아오신 것을 환영합니다", "en": "Welcome Back", "zh": "欢迎回来", "ja": "お帰りなさい",
        "ar": "مرحبًا بعودتك", "es": "Bienvenido de Vuelta", "hi": "वापसी पर स्वागत", "fr": "Bon Retour",
    },
    "create_account": {
        "ko": "계정 만들기", "en": "Create Account", "zh": "创建账号", "ja": "アカウント作成",
        "ar": "إنشاء حساب", "es": "Crear Cuenta", "hi": "खाता बनाएं", "fr": "Créer un Compte",
    },
    "login_subtitle": {
        "ko": "용진터보 정비 플랫폼에 로그인하세요", "en": "Sign in to YJT Maintenance Platform",
        "zh": "登录 YJT 维护平台", "ja": "YJTメンテナンスプラットフォームにログイン",
        "ar": "سجّل الدخول إلى منصة YJT للصيانة", "es": "Inicie sesión en la plataforma YJT",
        "hi": "YJT रखरखाव प्लेटफ़ॉर्म में साइन इन करें", "fr": "Connectez-vous à la plateforme YJT",
    },
    "register_subtitle": {
        "ko": "용진터보 정비 플랫폼에 가입하세요", "en": "Join YJT Maintenance Platform",
        "zh": "加入 YJT 维护平台", "ja": "YJTメンテナンスプラットフォームに登録",
        "ar": "انضم إلى منصة YJT للصيانة", "es": "Únase a la plataforma YJT",
        "hi": "YJT रखरखाव प्लेटफ़ॉर्म से जुड़ें", "fr": "Rejoignez la plateforme YJT",
    },

    # ── 비밀번호 찾기 (Forgot Password) ──
    "forgot_password": {
        "ko": "비밀번호를 잊으셨나요?", "en": "Forgot password?", "zh": "忘记密码？", "ja": "パスワードをお忘れですか？",
        "ar": "نسيت كلمة المرور؟", "es": "¿Olvidó su contraseña?", "hi": "पासवर्ड भूल गए?", "fr": "Mot de passe oublié ?",
    },
    "forgot_password_subtitle": {
        "ko": "이메일 주소를 입력하면 인증 코드를 보내드립니다", "en": "Enter your email and we'll send you a verification code",
        "zh": "输入您的电子邮箱，我们将发送验证码", "ja": "メールアドレスを入力すると認証コードをお送りします",
        "ar": "أدخل بريدك الإلكتروني وسنرسل لك رمز التحقق", "es": "Ingrese su correo y le enviaremos un código de verificación",
        "hi": "अपना ईमेल दर्ज करें और हम आपको सत्यापन कोड भेजेंगे", "fr": "Entrez votre e-mail et nous vous enverrons un code de vérification",
    },
    "send_code": {
        "ko": "인증 코드 발송", "en": "Send Code", "zh": "发送验证码", "ja": "認証コード送信",
        "ar": "إرسال الرمز", "es": "Enviar código", "hi": "कोड भेजें", "fr": "Envoyer le code",
    },
    "verification_code": {
        "ko": "인증 코드", "en": "Verification Code", "zh": "验证码", "ja": "認証コード",
        "ar": "رمز التحقق", "es": "Código de verificación", "hi": "सत्यापन कोड", "fr": "Code de vérification",
    },
    "new_password": {
        "ko": "새 비밀번호", "en": "New Password", "zh": "新密码", "ja": "新しいパスワード",
        "ar": "كلمة المرور الجديدة", "es": "Nueva contraseña", "hi": "नया पासवर्ड", "fr": "Nouveau mot de passe",
    },
    "confirm_password": {
        "ko": "비밀번호 확인", "en": "Confirm Password", "zh": "确认密码", "ja": "パスワード確認",
        "ar": "تأكيد كلمة المرور", "es": "Confirmar contraseña", "hi": "पासवर्ड की पुष्टि", "fr": "Confirmer le mot de passe",
    },
    "reset_password": {
        "ko": "비밀번호 변경", "en": "Reset Password", "zh": "重置密码", "ja": "パスワードリセット",
        "ar": "إعادة تعيين كلمة المرور", "es": "Restablecer contraseña", "hi": "पासवर्ड रीसेट", "fr": "Réinitialiser le mot de passe",
    },
    "code_sent": {
        "ko": "인증 코드가 이메일로 발송되었습니다", "en": "Verification code sent to your email", "zh": "验证码已发送到您的邮箱", "ja": "認証コードをメールに送信しました",
        "ar": "تم إرسال رمز التحقق إلى بريدك الإلكتروني", "es": "Código de verificación enviado a su correo", "hi": "सत्यापन कोड आपके ईमेल पर भेजा गया", "fr": "Code de vérification envoyé à votre e-mail",
    },
    "password_reset_success": {
        "ko": "비밀번호가 성공적으로 변경되었습니다", "en": "Password has been reset successfully", "zh": "密码已成功重置", "ja": "パスワードが正常にリセットされました",
        "ar": "تم إعادة تعيين كلمة المرور بنجاح", "es": "La contraseña se ha restablecido correctamente", "hi": "पासवर्ड सफलतापूर्वक रीसेट किया गया", "fr": "Le mot de passe a été réinitialisé avec succès",
    },
    "back_to_login": {
        "ko": "로그인으로 돌아가기", "en": "Back to Login", "zh": "返回登录", "ja": "ログインに戻る",
        "ar": "العودة إلى تسجيل الدخول", "es": "Volver al inicio de sesión", "hi": "लॉगिन पर वापस जाएं", "fr": "Retour à la connexion",
    },
    "password_mismatch": {
        "ko": "비밀번호가 일치하지 않습니다", "en": "Passwords do not match", "zh": "密码不匹配", "ja": "パスワードが一致しません",
        "ar": "كلمات المرور غير متطابقة", "es": "Las contraseñas no coinciden", "hi": "पासवर्ड मेल नहीं खाते", "fr": "Les mots de passe ne correspondent pas",
    },
    "verify": {
        "ko": "확인", "en": "Verify", "zh": "验证", "ja": "確認",
        "ar": "تحقق", "es": "Verificar", "hi": "सत्यापित करें", "fr": "Vérifier",
    },
    "resend_code": {
        "ko": "코드 재발송", "en": "Resend Code", "zh": "重新发送", "ja": "再送信",
        "ar": "إعادة إرسال", "es": "Reenviar", "hi": "दोबारा भेजें", "fr": "Renvoyer",
    },

    # ── 프로필 / 비밀번호 변경 (Profile / Change Password) ──
    "my_profile": {
        "ko": "내 프로필", "en": "My Profile", "zh": "我的资料", "ja": "マイプロフィール",
        "ar": "ملفي الشخصي", "es": "Mi Perfil", "hi": "मेरा प्रोफ़ाइल", "fr": "Mon Profil",
    },
    "edit_profile": {
        "ko": "프로필 수정", "en": "Edit Profile", "zh": "编辑资料", "ja": "プロフィール編集",
        "ar": "تعديل الملف الشخصي", "es": "Editar Perfil", "hi": "प्रोफ़ाइल संपादित करें", "fr": "Modifier le Profil",
    },
    "change_password": {
        "ko": "비밀번호 변경", "en": "Change Password", "zh": "更改密码", "ja": "パスワード変更",
        "ar": "تغيير كلمة المرور", "es": "Cambiar Contraseña", "hi": "पासवर्ड बदलें", "fr": "Changer le mot de passe",
    },
    "current_password": {
        "ko": "현재 비밀번호", "en": "Current Password", "zh": "当前密码", "ja": "現在のパスワード",
        "ar": "كلمة المرور الحالية", "es": "Contraseña Actual", "hi": "वर्तमान पासवर्ड", "fr": "Mot de passe actuel",
    },
    "password_changed": {
        "ko": "비밀번호가 변경되었습니다", "en": "Password changed successfully", "zh": "密码已更改", "ja": "パスワードが変更されました",
        "ar": "تم تغيير كلمة المرور بنجاح", "es": "Contraseña cambiada correctamente", "hi": "पासवर्ड सफलतापूर्वक बदला गया", "fr": "Mot de passe modifié avec succès",
    },
    "save": {
        "ko": "저장", "en": "Save", "zh": "保存", "ja": "保存",
        "ar": "حفظ", "es": "Guardar", "hi": "सहेजें", "fr": "Enregistrer",
    },
    "cancel": {
        "ko": "취소", "en": "Cancel", "zh": "取消", "ja": "キャンセル",
        "ar": "إلغاء", "es": "Cancelar", "hi": "रद्द करें", "fr": "Annuler",
    },
    "profile_updated": {
        "ko": "프로필이 업데이트되었습니다", "en": "Profile updated successfully", "zh": "资料已更新", "ja": "プロフィールが更新されました",
        "ar": "تم تحديث الملف الشخصي بنجاح", "es": "Perfil actualizado correctamente", "hi": "प्रोफ़ाइल सफलतापूर्वक अपडेट किया गया", "fr": "Profil mis à jour avec succès",
    },

    # ── 대시보드 (Dashboard) ──
    "total_parts": {
        "ko": "총 부품 수", "en": "Total Parts", "zh": "零件总数", "ja": "総部品数",
        "ar": "إجمالي القطع", "es": "Total de Piezas", "hi": "कुल पार्ट्स", "fr": "Total des Pièces",
    },
    "low_stock": {
        "ko": "재고 부족", "en": "Low Stock", "zh": "库存不足", "ja": "在庫不足",
        "ar": "مخزون منخفض", "es": "Stock Bajo", "hi": "कम स्टॉक", "fr": "Stock Faible",
    },
    "active_orders": {
        "ko": "진행 중 주문", "en": "Active Orders", "zh": "进行中订单", "ja": "進行中の注文",
        "ar": "الطلبات النشطة", "es": "Órdenes Activas", "hi": "सक्रिय ऑर्डर", "fr": "Commandes Actives",
    },
    "monthly_overhauls": {
        "ko": "월간 오버홀", "en": "Monthly Overhauls", "zh": "月度大修", "ja": "月間オーバーホール",
        "ar": "عمليات الصيانة الشهرية", "es": "Revisiones Mensuales", "hi": "मासिक ओवरहॉल", "fr": "Révisions Mensuelles",
    },

    # ── 챗봇 (Chatbot) ──
    "chat_title": {
        "ko": "AI 기술 어시스턴트", "en": "AI Technical Assistant", "zh": "AI 技术助手", "ja": "AI技術アシスタント",
        "ar": "مساعد تقني بالذكاء الاصطناعي", "es": "Asistente Técnico IA", "hi": "AI तकनीकी सहायक", "fr": "Assistant Technique IA",
    },
    "chat_placeholder": {
        "ko": "터보차저 관련 질문을 입력하세요...",
        "en": "Ask about turbocharger parts, service, or overhaul...",
        "zh": "请输入有关涡轮增压器的问题...",
        "ja": "ターボチャージャーに関する質問を入力してください...",
        "ar": "اسأل عن قطع غيار التوربو أو الصيانة...",
        "es": "Pregunte sobre piezas de turbocompresor, servicio u overhaul...",
        "hi": "टर्बोचार्जर पार्ट्स, सर्विस या ओवरहॉल के बारे में पूछें...",
        "fr": "Posez vos questions sur les turbocompresseurs...",
    },
    "chat_send": {
        "ko": "전송", "en": "Send", "zh": "发送", "ja": "送信",
        "ar": "إرسال", "es": "Enviar", "hi": "भेजें", "fr": "Envoyer",
    },
    "chat_error": {
        "ko": "죄송합니다, 응답 생성 중 오류가 발생했습니다. 다시 시도해주세요.",
        "en": "Sorry, an error occurred. Please try again.",
        "zh": "抱歉，生成回复时出错。请重试。",
        "ja": "申し訳ございません。エラーが発生しました。もう一度お試しください。",
        "ar": "عذرًا، حدث خطأ. يرجى المحاولة مرة أخرى.",
        "es": "Lo sentimos, ocurrió un error. Por favor, inténtelo de nuevo.",
        "hi": "क्षमा करें, एक त्रुटि हुई। कृपया पुनः प्रयास करें।",
        "fr": "Désolé, une erreur est survenue. Veuillez réessayer.",
    },

    # ── 재고 (Inventory) ──
    "search_parts": {
        "ko": "부품 검색...", "en": "Search parts...", "zh": "搜索零件...", "ja": "部品検索...",
        "ar": "البحث عن قطع...", "es": "Buscar piezas...", "hi": "पार्ट्स खोजें...", "fr": "Rechercher des pièces...",
    },
    "all_brands": {
        "ko": "전체 브랜드", "en": "All Brands", "zh": "所有品牌", "ja": "全ブランド",
        "ar": "جميع العلامات", "es": "Todas las Marcas", "hi": "सभी ब्रांड", "fr": "Toutes les Marques",
    },
    "part_name": {
        "ko": "부품명", "en": "Part Name", "zh": "零件名称", "ja": "部品名",
        "ar": "اسم القطعة", "es": "Nombre de Pieza", "hi": "पार्ट का नाम", "fr": "Nom de la Pièce",
    },
    "brand": {
        "ko": "브랜드", "en": "Brand", "zh": "品牌", "ja": "ブランド",
        "ar": "العلامة التجارية", "es": "Marca", "hi": "ब्रांड", "fr": "Marque",
    },
    "model": {
        "ko": "모델", "en": "Model", "zh": "型号", "ja": "モデル",
        "ar": "الطراز", "es": "Modelo", "hi": "मॉडल", "fr": "Modèle",
    },
    "stock": {
        "ko": "재고", "en": "Stock", "zh": "库存", "ja": "在庫",
        "ar": "المخزون", "es": "Stock", "hi": "स्टॉक", "fr": "Stock",
    },
    "price": {
        "ko": "단가", "en": "Unit Price", "zh": "单价", "ja": "単価",
        "ar": "سعر الوحدة", "es": "Precio Unitario", "hi": "इकाई मूल्य", "fr": "Prix Unitaire",
    },
    "status": {
        "ko": "상태", "en": "Status", "zh": "状态", "ja": "状態",
        "ar": "الحالة", "es": "Estado", "hi": "स्थिति", "fr": "Statut",
    },

    # ── 주문 (Orders) ──
    "all_status": {
        "ko": "전체 상태", "en": "All Status", "zh": "所有状态", "ja": "全ステータス",
        "ar": "جميع الحالات", "es": "Todos los Estados", "hi": "सभी स्थिति", "fr": "Tous les Statuts",
    },
    "pending": {
        "ko": "대기중", "en": "Pending", "zh": "待处理", "ja": "保留中",
        "ar": "قيد الانتظار", "es": "Pendiente", "hi": "लंबित", "fr": "En Attente",
    },
    "in_progress": {
        "ko": "진행중", "en": "In Progress", "zh": "进行中", "ja": "進行中",
        "ar": "قيد التنفيذ", "es": "En Progreso", "hi": "प्रगति में", "fr": "En Cours",
    },
    "completed": {
        "ko": "완료", "en": "Completed", "zh": "已完成", "ja": "完了",
        "ar": "مكتمل", "es": "Completado", "hi": "पूर्ण", "fr": "Terminé",
    },

    # ── 언어 선택 ──
    "select_language": {
        "ko": "언어 선택", "en": "Select Language", "zh": "选择语言", "ja": "言語選択",
        "ar": "اختر اللغة", "es": "Seleccionar Idioma", "hi": "भाषा चुनें", "fr": "Choisir la Langue",
    },

    # ── 환영 메시지 (Welcome) ──
    "welcome_user": {
        "ko": "님, 환영합니다!",
        "en": ", welcome!",
        "zh": "，欢迎您！",
        "ja": "さん、ようこそ！",
        "ar": "، مرحبًا بك!",
        "es": ", ¡bienvenido/a!",
        "hi": ", स्वागत है!",
        "fr": ", bienvenue !",
    },

    # ── 환영 팝업 (Welcome Modal) ──
    "welcome_modal_title": {
        "ko": "용진터보에 오신 것을 환영합니다!",
        "en": "Welcome to YONGJIN TURBO!",
        "zh": "欢迎来到龙津涡轮！",
        "ja": "ヨンジンターボへようこそ！",
        "ar": "!مرحبًا بكم في يونغجين توربو",
        "es": "¡Bienvenido a YONGJIN TURBO!",
        "hi": "योंगजिन टर्बो में आपका स्वागत है!",
        "fr": "Bienvenue chez YONGJIN TURBO !",
    },
    "welcome_modal_about": {
        "ko": "회사 소개",
        "en": "About Us",
        "zh": "关于我们",
        "ja": "会社紹介",
        "ar": "من نحن",
        "es": "Sobre Nosotros",
        "hi": "हमारे बारे में",
        "fr": "À Propos",
    },
    "welcome_modal_desc1": {
        "ko": "용진터보(YJT)는 부산 소재 터보차저 전문 기업으로, 선박용 터보차저의 오버홀, 부품 공급, 기술 서비스를 제공합니다.",
        "en": "YONGJIN TURBO (YJT) is a Busan-based turbocharger specialist company providing overhaul, parts supply, and technical services for marine turbochargers.",
        "zh": "龙津涡轮(YJT)是一家位于釜山的涡轮增压器专业公司，提供船舶涡轮增压器的大修、零件供应和技术服务。",
        "ja": "ヨンジンターボ(YJT)は釜山を拠点とするターボチャージャー専門企業で、船舶用ターボチャージャーのオーバーホール、部品供給、技術サービスを提供しています。",
        "ar": "يونغجين توربو (YJT) هي شركة متخصصة في الشواحن التوربينية مقرها بوسان، تقدم خدمات الصيانة الشاملة وتوريد القطع والخدمات الفنية للشواحن التوربينية البحرية.",
        "es": "YONGJIN TURBO (YJT) es una empresa especializada en turbocompresores con sede en Busan, que ofrece servicios de overhaul, suministro de piezas y servicios técnicos para turbocompresores marinos.",
        "hi": "योंगजिन टर्बो (YJT) बुसान स्थित एक टर्बोचार्जर विशेषज्ञ कंपनी है जो समुद्री टर्बोचार्जरों के ओवरहॉल, पार्ट्स सप्लाई और तकनीकी सेवाएं प्रदान करती है।",
        "fr": "YONGJIN TURBO (YJT) est une entreprise spécialisée en turbocompresseurs basée à Busan, offrant des services de révision, fourniture de pièces et services techniques pour turbocompresseurs marins.",
    },
    "welcome_modal_desc2": {
        "ko": "전 세계 31개국에 서비스를 제공하며, 연간 약 1,990건의 오버홀을 수행하고, $17M 규모의 부품 재고를 보유하고 있습니다.",
        "en": "We serve 31 countries worldwide, perform approximately 1,990 overhauls annually, and maintain $17M in parts inventory.",
        "zh": "我们为全球31个国家提供服务，每年执行约1,990次大修，并拥有价值1700万美元的零件库存。",
        "ja": "世界31カ国にサービスを提供し、年間約1,990件のオーバーホールを実施、1,700万ドル規模の部品在庫を保有しています。",
        "ar": "نخدم 31 دولة حول العالم، ونجري حوالي 1,990 عملية صيانة شاملة سنويًا، ونحتفظ بمخزون قطع غيار بقيمة 17 مليون دولار.",
        "es": "Servimos a 31 países en todo el mundo, realizamos aproximadamente 1,990 overhauls anuales y mantenemos un inventario de piezas de $17M.",
        "hi": "हम दुनिया भर के 31 देशों को सेवा प्रदान करते हैं, सालाना लगभग 1,990 ओवरहॉल करते हैं, और $17M के पार्ट्स इन्वेंटरी रखते हैं।",
        "fr": "Nous desservons 31 pays dans le monde, effectuons environ 1 990 révisions par an et maintenons un stock de pièces de 17 M$.",
    },
    "welcome_modal_brands": {
        "ko": "지원 브랜드",
        "en": "Supported Brands",
        "zh": "支持品牌",
        "ja": "対応ブランド",
        "ar": "العلامات التجارية المدعومة",
        "es": "Marcas Soportadas",
        "hi": "समर्थित ब्रांड",
        "fr": "Marques Supportées",
    },
    "welcome_modal_guide_title": {
        "ko": "플랫폼 사용법",
        "en": "How to Use",
        "zh": "使用指南",
        "ja": "プラットフォームの使い方",
        "ar": "دليل الاستخدام",
        "es": "Cómo Usar",
        "hi": "उपयोग कैसे करें",
        "fr": "Guide d'Utilisation",
    },
    "welcome_modal_guide_dashboard": {
        "ko": "대시보드 — 재고 현황, 주문 상태, 알림을 한눈에 확인하세요.",
        "en": "Dashboard — View inventory status, order status, and alerts at a glance.",
        "zh": "仪表盘 — 一览库存状态、订单状态和提醒。",
        "ja": "ダッシュボード — 在庫状況、注文状況、アラートを一目で確認できます。",
        "ar": "لوحة التحكم — عرض حالة المخزون وحالة الطلبات والتنبيهات بنظرة واحدة.",
        "es": "Panel — Visualice el estado del inventario, pedidos y alertas de un vistazo.",
        "hi": "डैशबोर्ड — इन्वेंटरी स्थिति, ऑर्डर स्थिति और अलर्ट एक नज़र में देखें।",
        "fr": "Tableau de bord — Visualisez l'état des stocks, des commandes et les alertes en un coup d'œil.",
    },
    "welcome_modal_guide_inventory": {
        "ko": "부품 재고 — MAN, MHI, KBB, ABB, Napier 등 브랜드별 부품을 검색하고 재고를 관리하세요.",
        "en": "Parts Inventory — Search and manage parts by brand: MAN, MHI, KBB, ABB, Napier, and more.",
        "zh": "零件库存 — 按品牌搜索和管理零件：MAN、MHI、KBB、ABB、Napier等。",
        "ja": "部品在庫 — MAN、MHI、KBB、ABB、Napierなどブランド別に部品を検索・管理できます。",
        "ar": "مخزون القطع — ابحث وأدر القطع حسب العلامة التجارية: MAN، MHI، KBB، ABB، Napier والمزيد.",
        "es": "Inventario de Piezas — Busque y gestione piezas por marca: MAN, MHI, KBB, ABB, Napier y más.",
        "hi": "पार्ट्स इन्वेंटरी — ब्रांड के अनुसार पार्ट्स खोजें और प्रबंधित करें: MAN, MHI, KBB, ABB, Napier आदि।",
        "fr": "Inventaire des Pièces — Recherchez et gérez les pièces par marque : MAN, MHI, KBB, ABB, Napier, etc.",
    },
    "welcome_modal_guide_chatbot": {
        "ko": "AI 어시스턴트 — 터보차저 기술 질문, 부품 조회, 오버홀 절차 등을 AI에게 물어보세요.",
        "en": "AI Assistant — Ask the AI about turbocharger technical questions, parts inquiries, overhaul procedures, and more.",
        "zh": "AI助手 — 向AI询问涡轮增压器技术问题、零件查询、大修程序等。",
        "ja": "AIアシスタント — ターボチャージャーの技術的な質問、部品照会、オーバーホール手順などをAIに質問できます。",
        "ar": "مساعد الذكاء الاصطناعي — اسأل الذكاء الاصطناعي عن الأسئلة التقنية للشاحن التوربيني واستفسارات القطع وإجراءات الصيانة.",
        "es": "Asistente IA — Pregunte al AI sobre cuestiones técnicas de turbocompresores, consultas de piezas, procedimientos de overhaul y más.",
        "hi": "AI सहायक — टर्बोचार्जर तकनीकी प्रश्न, पार्ट्स पूछताछ, ओवरहॉल प्रक्रियाएं और अधिक के बारे में AI से पूछें।",
        "fr": "Assistant IA — Posez vos questions à l'IA sur les turbocompresseurs, les pièces, les procédures de révision, etc.",
    },
    "welcome_modal_guide_orders": {
        "ko": "서비스 주문 — 오버홀, 부품 공급, 기술 서비스 주문 현황을 추적하세요.",
        "en": "Service Orders — Track overhaul, parts supply, and technical service order status.",
        "zh": "服务订单 — 跟踪大修、零件供应和技术服务订单状态。",
        "ja": "サービス注文 — オーバーホール、部品供給、技術サービスの注文状況を追跡できます。",
        "ar": "طلبات الخدمة — تتبع حالة طلبات الصيانة الشاملة وتوريد القطع والخدمات الفنية.",
        "es": "Órdenes de Servicio — Rastree el estado de overhaul, suministro de piezas y órdenes de servicio técnico.",
        "hi": "सेवा ऑर्डर — ओवरहॉल, पार्ट्स सप्लाई और तकनीकी सेवा ऑर्डर की स्थिति ट्रैक करें।",
        "fr": "Commandes de Service — Suivez l'état des révisions, fournitures de pièces et commandes de service technique.",
    },
    "welcome_modal_close": {
        "ko": "시작하기",
        "en": "Get Started",
        "zh": "开始使用",
        "ja": "始める",
        "ar": "ابدأ الآن",
        "es": "Comenzar",
        "hi": "शुरू करें",
        "fr": "Commencer",
    },
    "welcome_modal_dont_show": {
        "ko": "다시 보지 않기",
        "en": "Don't show again",
        "zh": "不再显示",
        "ja": "次回から表示しない",
        "ar": "عدم الإظهار مرة أخرى",
        "es": "No mostrar de nuevo",
        "hi": "दोबारा न दिखाएं",
        "fr": "Ne plus afficher",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Phase 2 추가 번역 키
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # ── 사이드바 확장 (Sidebar - Phase 2) ──
    "nav_customers": {
        "ko": "고객 관리", "en": "Customers", "zh": "客户管理", "ja": "顧客管理",
        "ar": "إدارة العملاء", "es": "Clientes", "hi": "ग्राहक प्रबंधन", "fr": "Clients",
    },
    "nav_analytics": {
        "ko": "분석", "en": "Analytics", "zh": "数据分析", "ja": "分析",
        "ar": "التحليلات", "es": "Analíticas", "hi": "विश्लेषिकी", "fr": "Analytique",
    },
    "nav_users": {
        "ko": "사용자 관리", "en": "User Management", "zh": "用户管理", "ja": "ユーザー管理",
        "ar": "إدارة المستخدمين", "es": "Gestión de Usuarios", "hi": "उपयोगकर्ता प्रबंधन", "fr": "Gestion des Utilisateurs",
    },
    "nav_my_orders": {
        "ko": "내 주문", "en": "My Orders", "zh": "我的订单", "ja": "マイオーダー",
        "ar": "طلباتي", "es": "Mis Pedidos", "hi": "मेरे ऑर्डर", "fr": "Mes Commandes",
    },
    "nav_notifications": {
        "ko": "알림", "en": "Notifications", "zh": "通知", "ja": "通知",
        "ar": "الإشعارات", "es": "Notificaciones", "hi": "सूचनाएं", "fr": "Notifications",
    },

    # ── 관리자 (Admin) ──
    "admin_badge": {
        "ko": "관리자", "en": "Admin", "zh": "管理员", "ja": "管理者",
        "ar": "مسؤول", "es": "Administrador", "hi": "व्यवस्थापक", "fr": "Administrateur",
    },
    "admin_only": {
        "ko": "관리자 전용 페이지입니다", "en": "This page is for administrators only",
        "zh": "此页面仅供管理员使用", "ja": "このページは管理者専用です",
        "ar": "هذه الصفحة مخصصة للمسؤولين فقط", "es": "Esta página es solo para administradores",
        "hi": "यह पृष्ठ केवल व्यवस्थापकों के लिए है", "fr": "Cette page est réservée aux administrateurs",
    },

    # ── CRUD 공통 ──
    "add": {
        "ko": "추가", "en": "Add", "zh": "添加", "ja": "追加",
        "ar": "إضافة", "es": "Agregar", "hi": "जोड़ें", "fr": "Ajouter",
    },
    "edit": {
        "ko": "수정", "en": "Edit", "zh": "编辑", "ja": "編集",
        "ar": "تعديل", "es": "Editar", "hi": "संपादित", "fr": "Modifier",
    },
    "delete": {
        "ko": "삭제", "en": "Delete", "zh": "删除", "ja": "削除",
        "ar": "حذف", "es": "Eliminar", "hi": "हटाएं", "fr": "Supprimer",
    },
    "save": {
        "ko": "저장", "en": "Save", "zh": "保存", "ja": "保存",
        "ar": "حفظ", "es": "Guardar", "hi": "सहेजें", "fr": "Enregistrer",
    },
    "cancel": {
        "ko": "취소", "en": "Cancel", "zh": "取消", "ja": "キャンセル",
        "ar": "إلغاء", "es": "Cancelar", "hi": "रद्द करें", "fr": "Annuler",
    },
    "create": {
        "ko": "생성", "en": "Create", "zh": "创建", "ja": "作成",
        "ar": "إنشاء", "es": "Crear", "hi": "बनाएं", "fr": "Créer",
    },
    "update": {
        "ko": "업데이트", "en": "Update", "zh": "更新", "ja": "更新",
        "ar": "تحديث", "es": "Actualizar", "hi": "अपडेट करें", "fr": "Mettre à jour",
    },
    "actions": {
        "ko": "작업", "en": "Actions", "zh": "操作", "ja": "操作",
        "ar": "إجراءات", "es": "Acciones", "hi": "कार्यवाही", "fr": "Actions",
    },
    "search": {
        "ko": "검색", "en": "Search", "zh": "搜索", "ja": "検索",
        "ar": "بحث", "es": "Buscar", "hi": "खोजें", "fr": "Rechercher",
    },
    "total": {
        "ko": "총", "en": "Total", "zh": "总计", "ja": "合計",
        "ar": "الإجمالي", "es": "Total", "hi": "कुल", "fr": "Total",
    },
    "no_data": {
        "ko": "데이터가 없습니다", "en": "No data found", "zh": "未找到数据", "ja": "データが見つかりません",
        "ar": "لم يتم العثور على بيانات", "es": "No se encontraron datos", "hi": "कोई डेटा नहीं मिला", "fr": "Aucune donnée trouvée",
    },
    "loading": {
        "ko": "로딩 중...", "en": "Loading...", "zh": "加载中...", "ja": "読み込み中...",
        "ar": "جاري التحميل...", "es": "Cargando...", "hi": "लोड हो रहा है...", "fr": "Chargement...",
    },

    # ── 부품 (Parts - CRUD) ──
    "add_part": {
        "ko": "부품 추가", "en": "Add Part", "zh": "添加零件", "ja": "部品追加",
        "ar": "إضافة قطعة", "es": "Agregar Pieza", "hi": "पार्ट जोड़ें", "fr": "Ajouter une Pièce",
    },
    "edit_part": {
        "ko": "부품 수정", "en": "Edit Part", "zh": "编辑零件", "ja": "部品編集",
        "ar": "تعديل القطعة", "es": "Editar Pieza", "hi": "पार्ट संपादित करें", "fr": "Modifier la Pièce",
    },
    "adjust_stock": {
        "ko": "재고 조정", "en": "Adjust Stock", "zh": "调整库存", "ja": "在庫調整",
        "ar": "تعديل المخزون", "es": "Ajustar Stock", "hi": "स्टॉक समायोजित करें", "fr": "Ajuster le Stock",
    },

    # ── 주문 (Orders - CRUD) ──
    "create_order": {
        "ko": "주문 생성", "en": "Create Order", "zh": "创建订单", "ja": "注文作成",
        "ar": "إنشاء طلب", "es": "Crear Pedido", "hi": "ऑर्डर बनाएं", "fr": "Créer une Commande",
    },
    "edit_order": {
        "ko": "주문 수정", "en": "Edit Order", "zh": "编辑订单", "ja": "注文編集",
        "ar": "تعديل الطلب", "es": "Editar Pedido", "hi": "ऑर्डर संपादित करें", "fr": "Modifier la Commande",
    },
    "order_type": {
        "ko": "주문 유형", "en": "Order Type", "zh": "订单类型", "ja": "注文タイプ",
        "ar": "نوع الطلب", "es": "Tipo de Pedido", "hi": "ऑर्डर प्रकार", "fr": "Type de Commande",
    },
    "vessel_name": {
        "ko": "선박명", "en": "Vessel Name", "zh": "船舶名称", "ja": "船名",
        "ar": "اسم السفينة", "es": "Nombre del Buque", "hi": "जहाज का नाम", "fr": "Nom du Navire",
    },

    # ── 고객 (Customers) ──
    "customer_management": {
        "ko": "고객 관리", "en": "Customer Management", "zh": "客户管理", "ja": "顧客管理",
        "ar": "إدارة العملاء", "es": "Gestión de Clientes", "hi": "ग्राहक प्रबंधन", "fr": "Gestion des Clients",
    },
    "add_customer": {
        "ko": "고객 추가", "en": "Add Customer", "zh": "添加客户", "ja": "顧客追加",
        "ar": "إضافة عميل", "es": "Agregar Cliente", "hi": "ग्राहक जोड़ें", "fr": "Ajouter un Client",
    },
    "company_name": {
        "ko": "회사명", "en": "Company Name", "zh": "公司名称", "ja": "会社名",
        "ar": "اسم الشركة", "es": "Nombre de Empresa", "hi": "कंपनी का नाम", "fr": "Nom de l'Entreprise",
    },
    "contact_name": {
        "ko": "담당자명", "en": "Contact Name", "zh": "联系人", "ja": "担当者名",
        "ar": "اسم جهة الاتصال", "es": "Nombre de Contacto", "hi": "संपर्क नाम", "fr": "Nom du Contact",
    },
    "vessel_type": {
        "ko": "선박 유형", "en": "Vessel Type", "zh": "船舶类型", "ja": "船種",
        "ar": "نوع السفينة", "es": "Tipo de Buque", "hi": "जहाज प्रकार", "fr": "Type de Navire",
    },

    # ── 문의 (Inquiries) ──
    "my_inquiries": {
        "ko": "내 문의", "en": "My Inquiries", "zh": "我的咨询", "ja": "お問い合わせ",
        "ar": "استفساراتي", "es": "Mis Consultas", "hi": "मेरी पूछताछ", "fr": "Mes Demandes",
    },
    "new_inquiry": {
        "ko": "새 문의", "en": "New Inquiry", "zh": "新咨询", "ja": "新規お問い合わせ",
        "ar": "استفسار جديد", "es": "Nueva Consulta", "hi": "नई पूछताछ", "fr": "Nouvelle Demande",
    },
    "respond": {
        "ko": "응답", "en": "Respond", "zh": "回复", "ja": "回答",
        "ar": "الرد", "es": "Responder", "hi": "जवाब दें", "fr": "Répondre",
    },
    "resolved": {
        "ko": "해결됨", "en": "Resolved", "zh": "已解决", "ja": "解決済み",
        "ar": "تم الحل", "es": "Resuelto", "hi": "हल किया गया", "fr": "Résolu",
    },
    "unresolved": {
        "ko": "미해결", "en": "Unresolved", "zh": "未解决", "ja": "未解決",
        "ar": "لم يتم الحل", "es": "Sin Resolver", "hi": "अनसुलझा", "fr": "Non Résolu",
    },

    # ── 알림 (Notifications) ──
    "notifications": {
        "ko": "알림", "en": "Notifications", "zh": "通知", "ja": "通知",
        "ar": "الإشعارات", "es": "Notificaciones", "hi": "सूचनाएं", "fr": "Notifications",
    },
    "mark_all_read": {
        "ko": "모두 읽음", "en": "Mark All Read", "zh": "全部已读", "ja": "すべて既読にする",
        "ar": "تعليم الكل كمقروء", "es": "Marcar Todo como Leído", "hi": "सभी पढ़ा हुआ चिह्नित करें", "fr": "Tout Marquer comme Lu",
    },
    "no_notifications": {
        "ko": "알림이 없습니다", "en": "No notifications", "zh": "没有通知", "ja": "通知はありません",
        "ar": "لا توجد إشعارات", "es": "Sin notificaciones", "hi": "कोई सूचना नहीं", "fr": "Aucune notification",
    },
    "view_all_notifications": {
        "ko": "모든 알림 보기", "en": "View all notifications", "zh": "查看所有通知", "ja": "すべての通知を見る",
        "ar": "عرض جميع الإشعارات", "es": "Ver todas las notificaciones", "hi": "सभी सूचनाएं देखें", "fr": "Voir toutes les notifications",
    },

    # ── 분석 (Analytics) ──
    "analytics_dashboard": {
        "ko": "분석 대시보드", "en": "Analytics Dashboard", "zh": "分析仪表盘", "ja": "分析ダッシュボード",
        "ar": "لوحة التحليلات", "es": "Panel de Analíticas", "hi": "विश्लेषिकी डैशबोर्ड", "fr": "Tableau de Bord Analytique",
    },
    "inventory_by_brand": {
        "ko": "브랜드별 재고", "en": "Inventory by Brand", "zh": "品牌库存", "ja": "ブランド別在庫",
        "ar": "المخزون حسب العلامة", "es": "Inventario por Marca", "hi": "ब्रांड अनुसार इन्वेंटरी", "fr": "Inventaire par Marque",
    },
    "order_status_dist": {
        "ko": "주문 상태 분포", "en": "Order Status Distribution", "zh": "订单状态分布", "ja": "注文状態分布",
        "ar": "توزيع حالة الطلبات", "es": "Distribución de Estado de Pedidos", "hi": "ऑर्डर स्थिति वितरण", "fr": "Distribution des Statuts de Commandes",
    },
    "monthly_orders_trend": {
        "ko": "월별 주문 추이", "en": "Monthly Orders Trend", "zh": "月度订单趋势", "ja": "月別注文推移",
        "ar": "اتجاه الطلبات الشهرية", "es": "Tendencia de Pedidos Mensuales", "hi": "मासिक ऑर्डर प्रवृत्ति", "fr": "Tendance des Commandes Mensuelles",
    },
    "inventory_value": {
        "ko": "재고 가치", "en": "Inventory Value", "zh": "库存价值", "ja": "在庫価値",
        "ar": "قيمة المخزون", "es": "Valor del Inventario", "hi": "इन्वेंटरी मूल्य", "fr": "Valeur du Stock",
    },
    "low_stock_summary": {
        "ko": "저재고 요약", "en": "Low Stock Summary", "zh": "低库存摘要", "ja": "在庫不足サマリー",
        "ar": "ملخص المخزون المنخفض", "es": "Resumen de Stock Bajo", "hi": "कम स्टॉक सारांश", "fr": "Résumé du Stock Faible",
    },
    "export_report": {
        "ko": "리포트 내보내기", "en": "Export Report", "zh": "导出报告", "ja": "レポート出力",
        "ar": "تصدير التقرير", "es": "Exportar Informe", "hi": "रिपोर्ट निर्यात", "fr": "Exporter le Rapport",
    },

    # ── 사용자 관리 (User Management) ──
    "user_management": {
        "ko": "사용자 관리", "en": "User Management", "zh": "用户管理", "ja": "ユーザー管理",
        "ar": "إدارة المستخدمين", "es": "Gestión de Usuarios", "hi": "उपयोगकर्ता प्रबंधन", "fr": "Gestion des Utilisateurs",
    },
    "toggle_admin": {
        "ko": "관리자 전환", "en": "Toggle Admin", "zh": "切换管理员", "ja": "管理者切替",
        "ar": "تبديل المسؤول", "es": "Alternar Admin", "hi": "व्यवस्थापक टॉगल", "fr": "Basculer Admin",
    },
    "role": {
        "ko": "역할", "en": "Role", "zh": "角色", "ja": "ロール",
        "ar": "الدور", "es": "Rol", "hi": "भूमिका", "fr": "Rôle",
    },
    "customer_role": {
        "ko": "고객", "en": "Customer", "zh": "客户", "ja": "顧客",
        "ar": "عميل", "es": "Cliente", "hi": "ग्राहक", "fr": "Client",
    },

    # ── 고객 대시보드 (Customer Dashboard) ──
    "quick_actions": {
        "ko": "빠른 액션", "en": "Quick Actions", "zh": "快速操作", "ja": "クイックアクション",
        "ar": "إجراءات سريعة", "es": "Acciones Rápidas", "hi": "त्वरित कार्यवाही", "fr": "Actions Rapides",
    },
    "ask_ai": {
        "ko": "AI에게 질문하기", "en": "Ask AI Assistant", "zh": "向AI提问", "ja": "AIに質問する",
        "ar": "اسأل المساعد الذكي", "es": "Preguntar al Asistente IA", "hi": "AI सहायक से पूछें", "fr": "Demander à l'Assistant IA",
    },
    "view_my_orders": {
        "ko": "내 주문 보기", "en": "View My Orders", "zh": "查看我的订单", "ja": "マイオーダーを見る",
        "ar": "عرض طلباتي", "es": "Ver Mis Pedidos", "hi": "मेरे ऑर्डर देखें", "fr": "Voir Mes Commandes",
    },
    "submit_inquiry": {
        "ko": "문의하기", "en": "Submit Inquiry", "zh": "提交咨询", "ja": "お問い合わせを送信",
        "ar": "إرسال استفسار", "es": "Enviar Consulta", "hi": "पूछताछ सबमिट करें", "fr": "Soumettre une Demande",
    },
    "recent_orders": {
        "ko": "최근 주문", "en": "Recent Orders", "zh": "最近订单", "ja": "最近の注文",
        "ar": "الطلبات الأخيرة", "es": "Pedidos Recientes", "hi": "हालिया ऑर्डर", "fr": "Commandes Récentes",
    },
    "recent_inquiries": {
        "ko": "최근 문의", "en": "Recent Inquiries", "zh": "最近咨询", "ja": "最近のお問い合わせ",
        "ar": "الاستفسارات الأخيرة", "es": "Consultas Recientes", "hi": "हालिया पूछताछ", "fr": "Demandes Récentes",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Phase 3 - 선박/장비/PMS/운전시간 번역 키
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # ── 선박 (Vessels) ──
    "nav_vessels": {
        "ko": "선박 관리", "en": "Vessels", "zh": "船舶管理", "ja": "船舶管理",
        "ar": "إدارة السفن", "es": "Buques", "hi": "जहाज प्रबंधन", "fr": "Navires",
    },
    "vessels": {
        "ko": "선박", "en": "Vessels", "zh": "船舶", "ja": "船舶",
        "ar": "السفن", "es": "Buques", "hi": "जहाज", "fr": "Navires",
    },
    "add_vessel": {
        "ko": "선박 추가", "en": "Add Vessel", "zh": "添加船舶", "ja": "船舶追加",
        "ar": "إضافة سفينة", "es": "Agregar Buque", "hi": "जहाज जोड़ें", "fr": "Ajouter un Navire",
    },
    "imo_number": {
        "ko": "IMO 번호", "en": "IMO Number", "zh": "IMO编号", "ja": "IMO番号",
        "ar": "رقم IMO", "es": "Número IMO", "hi": "IMO नंबर", "fr": "Numéro IMO",
    },
    "class_society": {
        "ko": "선급", "en": "Class Society", "zh": "船级社", "ja": "船級",
        "ar": "جمعية التصنيف", "es": "Sociedad de Clasificación", "hi": "वर्ग समाज", "fr": "Société de Classification",
    },
    "flag": {
        "ko": "선적항", "en": "Flag", "zh": "船旗", "ja": "旗国",
        "ar": "العلم", "es": "Bandera", "hi": "ध्वज", "fr": "Pavillon",
    },
    "owner": {
        "ko": "선주", "en": "Owner", "zh": "船东", "ja": "船主",
        "ar": "المالك", "es": "Propietario", "hi": "मालिक", "fr": "Propriétaire",
    },
    "manager": {
        "ko": "관리 회사", "en": "Manager", "zh": "管理公司", "ja": "管理会社",
        "ar": "المدير", "es": "Administrador", "hi": "प्रबंधक", "fr": "Gestionnaire",
    },

    # ── 장비 (Equipment) ──
    "nav_equipment": {
        "ko": "장비 관리", "en": "Equipment", "zh": "设备管理", "ja": "機器管理",
        "ar": "إدارة المعدات", "es": "Equipos", "hi": "उपकरण प्रबंधन", "fr": "Équipements",
    },
    "equipment": {
        "ko": "장비", "en": "Equipment", "zh": "设备", "ja": "機器",
        "ar": "المعدات", "es": "Equipo", "hi": "उपकरण", "fr": "Équipement",
    },
    "equipment_tree": {
        "ko": "장비 트리", "en": "Equipment Tree", "zh": "设备树", "ja": "機器ツリー",
        "ar": "شجرة المعدات", "es": "Árbol de Equipos", "hi": "उपकरण वृक्ष", "fr": "Arborescence des Équipements",
    },
    "equipment_code": {
        "ko": "장비 코드", "en": "Equipment Code", "zh": "设备代码", "ja": "機器コード",
        "ar": "رمز المعدات", "es": "Código de Equipo", "hi": "उपकरण कोड", "fr": "Code Équipement",
    },
    "maker": {
        "ko": "제조사", "en": "Maker", "zh": "制造商", "ja": "メーカー",
        "ar": "الشركة المصنعة", "es": "Fabricante", "hi": "निर्माता", "fr": "Fabricant",
    },
    "serial_number": {
        "ko": "시리얼 번호", "en": "Serial Number", "zh": "序列号", "ja": "シリアル番号",
        "ar": "الرقم التسلسلي", "es": "Número de Serie", "hi": "सीरियल नंबर", "fr": "Numéro de Série",
    },
    "category": {
        "ko": "카테고리", "en": "Category", "zh": "类别", "ja": "カテゴリー",
        "ar": "الفئة", "es": "Categoría", "hi": "श्रेणी", "fr": "Catégorie",
    },

    # ── 운전시간 (Running Hours) ──
    "nav_running_hours": {
        "ko": "운전시간", "en": "Running Hours", "zh": "运行时间", "ja": "運転時間",
        "ar": "ساعات التشغيل", "es": "Horas de Funcionamiento", "hi": "चलने के घंटे", "fr": "Heures de Fonctionnement",
    },
    "running_hours": {
        "ko": "운전시간", "en": "Running Hours", "zh": "运行时间", "ja": "運転時間",
        "ar": "ساعات التشغيل", "es": "Horas de Funcionamiento", "hi": "चलने के घंटे", "fr": "Heures de Fonctionnement",
    },
    "daily_hours": {
        "ko": "일일 운전시간", "en": "Daily Hours", "zh": "每日运行时间", "ja": "日次運転時間",
        "ar": "ساعات التشغيل اليومية", "es": "Horas Diarias", "hi": "दैनिक घंटे", "fr": "Heures Journalières",
    },
    "total_hours": {
        "ko": "누적 시간", "en": "Total Hours", "zh": "累计时间", "ja": "累計時間",
        "ar": "إجمالي الساعات", "es": "Horas Totales", "hi": "कुल घंटे", "fr": "Heures Totales",
    },
    "record_hours": {
        "ko": "시간 기록", "en": "Record Hours", "zh": "记录时间", "ja": "時間記録",
        "ar": "تسجيل الساعات", "es": "Registrar Horas", "hi": "घंटे दर्ज करें", "fr": "Enregistrer les Heures",
    },

    # ── PMS (정비 계획 관리) ──
    "nav_pms": {
        "ko": "PMS", "en": "PMS", "zh": "PMS", "ja": "PMS",
        "ar": "PMS", "es": "PMS", "hi": "PMS", "fr": "PMS",
    },
    "maintenance_plan": {
        "ko": "정비 계획", "en": "Maintenance Plan", "zh": "维护计划", "ja": "整備計画",
        "ar": "خطة الصيانة", "es": "Plan de Mantenimiento", "hi": "रखरखाव योजना", "fr": "Plan de Maintenance",
    },
    "maintenance_plans": {
        "ko": "정비 계획", "en": "Maintenance Plans", "zh": "维护计划", "ja": "整備計画一覧",
        "ar": "خطط الصيانة", "es": "Planes de Mantenimiento", "hi": "रखरखाव योजनाएं", "fr": "Plans de Maintenance",
    },

    # ── 작업지시서 (Work Orders) ──
    "nav_work_orders": {
        "ko": "작업지시서", "en": "Work Orders", "zh": "工作指令", "ja": "作業指示書",
        "ar": "أوامر العمل", "es": "Órdenes de Trabajo", "hi": "कार्य आदेश", "fr": "Ordres de Travail",
    },
    "work_orders": {
        "ko": "작업지시서", "en": "Work Orders", "zh": "工作指令", "ja": "作業指示書",
        "ar": "أوامر العمل", "es": "Órdenes de Trabajo", "hi": "कार्य आदेश", "fr": "Ordres de Travail",
    },
    "planned": {
        "ko": "계획됨", "en": "Planned", "zh": "已计划", "ja": "計画済み",
        "ar": "مخطط", "es": "Planificado", "hi": "नियोजित", "fr": "Planifié",
    },
    "overdue": {
        "ko": "초과", "en": "Overdue", "zh": "逾期", "ja": "超過",
        "ar": "متأخر", "es": "Vencido", "hi": "अतिदेय", "fr": "En Retard",
    },
    "postponed": {
        "ko": "연기됨", "en": "Postponed", "zh": "已推迟", "ja": "延期",
        "ar": "مؤجل", "es": "Pospuesto", "hi": "स्थगित", "fr": "Reporté",
    },
    "priority": {
        "ko": "우선순위", "en": "Priority", "zh": "优先级", "ja": "優先度",
        "ar": "الأولوية", "es": "Prioridad", "hi": "प्राथमिकता", "fr": "Priorité",
    },
    "critical": {
        "ko": "긴급", "en": "Critical", "zh": "紧急", "ja": "緊急",
        "ar": "حرج", "es": "Crítico", "hi": "गंभीर", "fr": "Critique",
    },
    "high": {
        "ko": "높음", "en": "High", "zh": "高", "ja": "高",
        "ar": "عالي", "es": "Alto", "hi": "उच्च", "fr": "Élevé",
    },
    "medium": {
        "ko": "보통", "en": "Medium", "zh": "中", "ja": "中",
        "ar": "متوسط", "es": "Medio", "hi": "मध्यम", "fr": "Moyen",
    },
    "low": {
        "ko": "낮음", "en": "Low", "zh": "低", "ja": "低",
        "ar": "منخفض", "es": "Bajo", "hi": "कम", "fr": "Faible",
    },
    "due_date": {
        "ko": "마감일", "en": "Due Date", "zh": "截止日期", "ja": "期限",
        "ar": "تاريخ الاستحقاق", "es": "Fecha de Vencimiento", "hi": "नियत तारीख", "fr": "Date d'Échéance",
    },
    "planned_date": {
        "ko": "계획일", "en": "Planned Date", "zh": "计划日期", "ja": "計画日",
        "ar": "التاريخ المخطط", "es": "Fecha Planificada", "hi": "नियोजित तिथि", "fr": "Date Prévue",
    },
    "completed_date": {
        "ko": "완료일", "en": "Completed Date", "zh": "完成日期", "ja": "完了日",
        "ar": "تاريخ الإنجاز", "es": "Fecha de Finalización", "hi": "पूर्ण होने की तिथि", "fr": "Date d'Achèvement",
    },
    "completion_rate": {
        "ko": "완료율", "en": "Completion Rate", "zh": "完成率", "ja": "完了率",
        "ar": "نسبة الإنجاز", "es": "Tasa de Completación", "hi": "पूर्णता दर", "fr": "Taux d'Achèvement",
    },
    "class_related": {
        "ko": "선급 관련", "en": "Class Related", "zh": "船级相关", "ja": "船級関連",
        "ar": "متعلق بالتصنيف", "es": "Relacionado con Clase", "hi": "वर्ग संबंधित", "fr": "Lié à la Classification",
    },
    "overhaul_progress": {
        "ko": "오버홀 진행률", "en": "Overhaul Progress", "zh": "大修进度", "ja": "オーバーホール進捗",
        "ar": "تقدم الصيانة الشاملة", "es": "Progreso de Overhaul", "hi": "ओवरहॉल प्रगति", "fr": "Progression de la Révision",
    },
    "upcoming": {
        "ko": "예정", "en": "Upcoming", "zh": "即将到来", "ja": "予定",
        "ar": "القادم", "es": "Próximo", "hi": "आगामी", "fr": "À Venir",
    },

    # ── 역할 (Roles) ──
    "role_admin": {
        "ko": "관리자", "en": "Admin", "zh": "管理员", "ja": "管理者",
        "ar": "مسؤول", "es": "Administrador", "hi": "व्यवस्थापक", "fr": "Administrateur",
    },
    "role_captain": {
        "ko": "선장", "en": "Captain", "zh": "船长", "ja": "船長",
        "ar": "القبطان", "es": "Capitán", "hi": "कप्तान", "fr": "Capitaine",
    },
    "role_chief_engineer": {
        "ko": "기관장", "en": "Chief Engineer", "zh": "轮机长", "ja": "機関長",
        "ar": "كبير المهندسين", "es": "Jefe de Máquinas", "hi": "मुख्य इंजीनियर", "fr": "Chef Mécanicien",
    },
    "role_shore_manager": {
        "ko": "육상 관리자", "en": "Shore Manager", "zh": "岸上管理员", "ja": "陸上管理者",
        "ar": "مدير الشاطئ", "es": "Gerente de Costa", "hi": "तट प्रबंधक", "fr": "Responsable à Terre",
    },
    "role_engineer": {
        "ko": "엔지니어", "en": "Engineer", "zh": "工程师", "ja": "エンジニア",
        "ar": "مهندس", "es": "Ingeniero", "hi": "इंजीनियर", "fr": "Ingénieur",
    },
    "role_customer": {
        "ko": "고객", "en": "Customer", "zh": "客户", "ja": "顧客",
        "ar": "عميل", "es": "Cliente", "hi": "ग्राहक", "fr": "Client",
    },

    # ── 대시보드 확장 (Dashboard - Phase 3) ──
    "vessel_dashboard": {
        "ko": "선박 대시보드", "en": "Vessel Dashboard", "zh": "船舶仪表盘", "ja": "船舶ダッシュボード",
        "ar": "لوحة السفينة", "es": "Panel del Buque", "hi": "जहाज डैशबोर्ड", "fr": "Tableau de Bord du Navire",
    },
    "pms_overdue": {
        "ko": "PMS 초과", "en": "PMS Overdue", "zh": "PMS逾期", "ja": "PMS超過",
        "ar": "PMS متأخر", "es": "PMS Vencido", "hi": "PMS अतिदेय", "fr": "PMS en Retard",
    },
    "pending_orders": {
        "ko": "대기 주문", "en": "Pending Orders", "zh": "待处理订单", "ja": "保留中の注文",
        "ar": "الطلبات المعلقة", "es": "Pedidos Pendientes", "hi": "लंबित ऑर्डर", "fr": "Commandes en Attente",
    },
    "completed_orders": {
        "ko": "완료 주문", "en": "Completed Orders", "zh": "已完成订单", "ja": "完了した注文",
        "ar": "الطلبات المكتملة", "es": "Pedidos Completados", "hi": "पूर्ण ऑर्डर", "fr": "Commandes Terminées",
    },
}


def get_translation(key: str, lang: str = "en") -> str:
    """번역 키로 해당 언어의 텍스트를 반환"""
    if key in TRANSLATIONS:
        return TRANSLATIONS[key].get(lang, TRANSLATIONS[key].get("en", key))
    return key


def get_all_translations(lang: str = "en") -> dict:
    """특정 언어의 모든 번역을 반환"""
    result = {}
    for key, translations in TRANSLATIONS.items():
        result[key] = translations.get(lang, translations.get("en", key))
    return result
