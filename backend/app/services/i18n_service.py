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
