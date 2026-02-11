import type { NextConfig } from "next";

// 백엔드 API URL: 프로덕션(Render)에서는 환경변수, 로컬에서는 localhost
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const nextConfig: NextConfig = {
  // ── API 프록시 설정 ──
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${API_URL}/api/:path*`,
      },
    ];
  },

  // ── HTTP keep-alive 설정 (CLOSE_WAIT 방지) ──
  httpAgentOptions: {
    keepAlive: true,          // 커넥션 재사용 활성화
  },

  // ── 핫 리로드 최적화 (불필요한 재빌드 방지 → 커넥션 낭비 감소) ──
  webpack: (config, { dev }) => {
    if (dev) {
      // watchOptions: 파일 변경 감지 최적화
      config.watchOptions = {
        ...config.watchOptions,
        poll: false,              // 폴링 비활성화 (기본 inotify 사용)
        aggregateTimeout: 500,    // 변경 감지 후 500ms 대기 후 리빌드 (연속 저장 대응)
        ignored: [
          "**/node_modules/**",
          "**/.next/**",
          "**/.git/**",
        ],
      };
    }
    return config;
  },

  // ── 서버 외부 패키지 (Next.js 15+에서 experimental 밖으로 이동) ──
  serverExternalPackages: [],
};

export default nextConfig;
