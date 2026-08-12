# Buzz ACP 에이전트 하네스 이미지.
#
# 공개 릴레이 이미지(ghcr.io/block/buzz)에는 buzz-relay / buzz-admin /
# buzz-pair-relay 만 들어 있고 buzz-cli(`buzz`)와 buzz-acp 는 없다. 그래서
# 에이전트 쪽은 소스에서 직접 빌드한다.
#
# 구조:  Buzz Relay ──WS──> buzz-acp ──stdio──> claude-agent-acp ──> Claude
#                                        └─ 에이전트는 `buzz` CLI 로 응답/작업
#
# 빌드 (최초 1회, Rust 워크스페이스 컴파일이라 15~40분 소요):
#   docker build -t yjt-buzz-agent:latest infra/buzz/agent

ARG RUST_VERSION=1.95
ARG NODE_VERSION=24
ARG DEBIAN_VERSION=bookworm

# ─── 1) buzz-cli + buzz-acp 빌드 ──────────────────────────────────────────
FROM rust:${RUST_VERSION}-${DEBIAN_VERSION} AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        pkg-config \
        libssl-dev \
        ca-certificates \
        git \
    && rm -rf /var/lib/apt/lists/*

# 릴레이와 같은 리비전으로 맞추고 싶으면 --build-arg BUZZ_REF=<tag|sha> 사용.
ARG BUZZ_REF=main
WORKDIR /build
RUN git clone --depth 1 --branch "${BUZZ_REF}" https://github.com/block/buzz.git .

RUN cargo build --release --locked \
        -p buzz-cli --bin buzz \
        -p buzz-acp --bin buzz-acp

# ─── 2) 런타임 ────────────────────────────────────────────────────────────
FROM node:${NODE_VERSION}-${DEBIAN_VERSION}-slim AS runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        git \
        ca-certificates \
        curl \
        jq \
        openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Claude Agent SDK 를 ACP 로 감싸는 어댑터. buzz-acp 가 이 명령을 stdio 로 띄운다.
RUN npm install -g @agentclientprotocol/claude-agent-acp

COPY --from=builder /build/target/release/buzz     /usr/local/bin/buzz
COPY --from=builder /build/target/release/buzz-acp /usr/local/bin/buzz-acp

RUN useradd --create-home --shell /bin/bash agent \
    && mkdir -p /workspace \
    && chown agent:agent /workspace

USER agent
WORKDIR /workspace

# claude-agent-acp 는 인자 없이 실행된다(buzz-acp 가 기본 "acp" 인자를 걷어냄).
ENV BUZZ_ACP_AGENT_COMMAND=claude-agent-acp \
    BUZZ_RELAY_URL=ws://relay:3000

ENTRYPOINT ["buzz-acp"]
