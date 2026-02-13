"use client";

import { useState, useRef, useEffect } from "react";
import { sendChatMessage } from "@/lib/api";
import { useI18n } from "@/lib/i18n";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const WELCOME_MESSAGES: Record<string, string> = {
  ko: "안녕하세요! 용진터보 AI 어시스턴트입니다.\n\n다음과 같은 도움을 드릴 수 있습니다:\n- 부품 재고 조회 (예: 'MAN NR29/S 베어링 재고')\n- 오버홀 서비스 안내\n- 기술 문의\n- 연락처 안내\n\n무엇을 도와드릴까요?",
  en: "Hello! I'm the YJT AI Assistant.\n\nI can help you with:\n- Parts inventory inquiry (e.g., 'MAN NR29/S bearing stock')\n- Overhaul service information\n- Technical inquiries\n- Contact information\n\nHow can I assist you?",
  zh: "您好！我是 YJT AI 助手。\n\n我可以为您提供以下帮助：\n- 零件库存查询（例：'MAN NR29/S 轴承库存'）\n- 大修服务信息\n- 技术咨询\n- 联系方式\n\n请问有什么可以帮助您的？",
  ja: "こんにちは！YJT AIアシスタントです。\n\n以下のお手伝いが可能です：\n- 部品在庫照会（例：'MAN NR29/S ベアリング在庫'）\n- オーバーホールサービスのご案内\n- 技術的なお問い合わせ\n- お問い合わせ先のご案内\n\nご質問をどうぞ！",
  ar: "مرحبًا! أنا مساعد YJT الذكي.\n\nيمكنني مساعدتك في:\n- استعلام مخزون القطع (مثال: 'MAN NR29/S مخزون المحامل')\n- معلومات خدمة الصيانة الشاملة\n- الاستفسارات الفنية\n- معلومات الاتصال\n\nكيف يمكنني مساعدتك؟",
  es: "¡Hola! Soy el Asistente IA de YJT.\n\nPuedo ayudarle con:\n- Consulta de inventario de piezas (ej: 'stock de rodamientos MAN NR29/S')\n- Información de servicio de overhaul\n- Consultas técnicas\n- Información de contacto\n\n¿En qué puedo ayudarle?",
  hi: "नमस्ते! मैं YJT AI सहायक हूँ।\n\nमैं आपकी इन बातों में मदद कर सकता हूँ:\n- पार्ट्स इन्वेंटरी पूछताछ (उदा: 'MAN NR29/S बेयरिंग स्टॉक')\n- ओवरहॉल सेवा जानकारी\n- तकनीकी पूछताछ\n- संपर्क जानकारी\n\nमैं आपकी कैसे सहायता कर सकता हूँ?",
  fr: "Bonjour ! Je suis l'Assistant IA YJT.\n\nJe peux vous aider avec :\n- Consultation de stock de pièces (ex : 'stock roulements MAN NR29/S')\n- Informations sur le service de révision\n- Questions techniques\n- Coordonnées\n\nComment puis-je vous aider ?",
};

export default function ChatbotPage() {
  const { t, lang } = useI18n();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 언어 변경 시 초기 메시지 갱신
  useEffect(() => {
    setMessages([
      {
        role: "assistant",
        content: WELCOME_MESSAGES[lang] || WELCOME_MESSAGES.en,
      },
    ]);
  }, [lang]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg: Message = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const history = messages.map((m) => ({
        role: m.role,
        content: m.content,
      }));
      const { response } = await sendChatMessage(userMsg.content, history, lang);
      setMessages((prev) => [...prev, { role: "assistant", content: response }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: t("chat_error") },
      ]);
    } finally {
      setLoading(false);
    }
  }

  const suggestions: Record<string, string[]> = {
    ko: ["MAN NR29/S 베어링 재고 확인", "오버홀 서비스 절차 안내", "KBB HPR 시리즈 부품 가격", "긴급 엔지니어 파견 문의"],
    en: ["MAN NR29/S bearing stock", "Overhaul procedure", "KBB HPR series pricing", "Emergency engineer dispatch"],
    zh: ["MAN NR29/S 轴承库存", "大修服务流程", "KBB HPR系列价格", "紧急工程师派遣"],
    ja: ["MAN NR29/S ベアリング在庫", "オーバーホール手順", "KBB HPRシリーズ価格", "緊急エンジニア派遣"],
    ar: ["مخزون محامل MAN NR29/S", "إجراءات الصيانة الشاملة", "أسعار سلسلة KBB HPR", "إرسال مهندس طوارئ"],
    es: ["Stock rodamientos MAN NR29/S", "Procedimiento de overhaul", "Precios serie KBB HPR", "Despacho ingeniero urgente"],
    hi: ["MAN NR29/S बेयरिंग स्टॉक", "ओवरहॉल प्रक्रिया", "KBB HPR सीरीज़ कीमत", "आपातकालीन इंजीनियर"],
    fr: ["Stock roulements MAN NR29/S", "Procédure de révision", "Prix série KBB HPR", "Envoi ingénieur urgence"],
  };

  const currentSuggestions = suggestions[lang] || suggestions.en;

  return (
    <div className="h-[calc(100vh-7rem)] sm:h-[calc(100vh-8rem)] flex flex-col">
      <h1 className="text-xl sm:text-2xl font-bold text-gray-800 mb-3 sm:mb-4">
        {t("chat_title")}
      </h1>

      {/* Chat Area */}
      <div className="flex-1 bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col overflow-hidden min-h-0">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-3 sm:p-6 space-y-3 sm:space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              } animate-fade-in`}
            >
              <div
                className={`max-w-[85%] sm:max-w-[70%] rounded-2xl px-3 py-2 sm:px-4 sm:py-3 ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-800"
                }`}
              >
                {msg.role === "assistant" && (
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-semibold text-blue-600">
                      YJT AI
                    </span>
                  </div>
                )}
                <div className="text-xs sm:text-sm whitespace-pre-wrap leading-relaxed">
                  {msg.content}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start animate-fade-in">
              <div className="bg-gray-100 rounded-2xl px-4 py-3">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }} />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }} />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions */}
        {messages.length <= 1 && (
          <div className="px-3 sm:px-6 pb-2 sm:pb-3 flex flex-wrap gap-1.5 sm:gap-2">
            {currentSuggestions.map((s) => (
              <button
                key={s}
                onClick={() => setInput(s)}
                className="px-2 py-1 sm:px-3 sm:py-1.5 bg-blue-50 text-blue-600 rounded-full text-[11px] sm:text-xs font-medium hover:bg-blue-100 transition-colors"
              >
                {s}
              </button>
            ))}
          </div>
        )}

        {/* Input */}
        <form onSubmit={handleSend} className="p-2 sm:p-4 border-t border-gray-200 flex gap-2 sm:gap-3 safe-bottom">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t("chat_placeholder")}
            className="flex-1 min-w-0 px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="px-4 py-2 sm:px-6 sm:py-3 bg-blue-600 text-white rounded-xl text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex-shrink-0"
          >
            {t("chat_send")}
          </button>
        </form>
      </div>
    </div>
  );
}
