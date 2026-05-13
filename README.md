<p align="center">
  <img src="https://raw.githubusercontent.com/redchupa/kakao-noti/main/images/logo.png" alt="Kakao Notify Logo" width="640">
</p>

<p align="center">
  <a href="https://github.com/hacs/integration"><img src="https://img.shields.io/badge/HACS-Custom-41BDF5.svg" alt="HACS"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/redchupa/kakao-noti" alt="License"></a>
  <a href="https://github.com/redchupa/kakao-noti/stargazers"><img src="https://img.shields.io/github/stars/redchupa/kakao-noti?style=social" alt="Stars"></a>
</p>

# 카카오톡 나에게 보내기 — Home Assistant 알림

Home Assistant에서 자동화·스크립트가 작동하면 **내 카카오톡 "나와의 채팅"** 으로 메시지가 도착하게 만드는 통합입니다.
텔레그램 봇 알림을 카톡으로 받는 셈이에요.

```yaml
# 자동화나 스크립트에서 이 한 줄만 추가하면 카톡으로 도착해요
service: notify.kakao_noti
data:
  message: "현관문이 열렸어요"
```

> 💬 이 통합은 **본인 카카오톡 "나와의 채팅"** 으로만 메시지를 보냅니다.
> 친구·가족 카톡으로 보내는 게 아니라 **내가 나에게** 보내는 형태입니다.
> ("나와의 채팅"은 카카오톡 채팅 목록 맨 위에 있는 본인 프로필 채팅방이에요.)

---

## 📑 목차

- [이 가이드를 따라가면 무엇이 됩니까](#-이-가이드를-따라가면-무엇이-됩니까)
- [시작 전 알아둘 것 (꼭 읽어주세요)](#-시작-전-알아둘-것-꼭-읽어주세요)
- [1단계 · 카카오 디벨로퍼스에서 앱 만들기](#1단계--카카오-디벨로퍼스에서-앱-만들기)
- [2단계 · HACS로 컴포넌트 설치](#2단계--hacs로-컴포넌트-설치)
- [3단계 · HA에서 카카오 연결](#3단계--ha에서-카카오-연결)
- [4단계 · 첫 메시지 보내기](#4단계--첫-메시지-보내기)
- [실전 사용 예시](#실전-사용-예시)
- [가족·여러 명에게 보내기 (멀티 계정)](#가족여러-명에게-보내기-멀티-계정)
- [토큰은 자동으로 갱신돼요](#토큰은-자동으로-갱신돼요)
- [잘 안 될 때](#잘-안-될-때)
- [자주 묻는 질문](#자주-묻는-질문)
- [후원](#후원)
- [라이선스](#라이선스)

---

## ✨ 이 가이드를 따라가면 무엇이 됩니까

- **자동화 / 스크립트에서** `notify.kakao_noti` 한 줄로 카톡 발송
- **여러 줄·이모지·제목 지원**, 1850자 넘으면 자동 절단
- **카카오 로그인 토큰 자동 갱신** (HA가 다 알아서 해줌)
- **별도 서버·애드온 불필요** — HA 내부에서 카카오와 직접 통신
- **여러 가족 구성원** 각자 자기 카톡으로 받을 수 있게 멀티 계정 지원

> ⏱️ 끝까지 따라하는 데 **30~40분** 정도. 카카오 콘솔 설정이 처음이면 좀 더 걸릴 수 있어요.

---

## 🧭 시작 전 알아둘 것 (꼭 읽어주세요)

| | |
|---|---|
| **Home Assistant** | 이 통합이 동작할 곳. 아직 없으시면 → ▶ **[Home Assistant 입문 가이드 (한국어, 블로그)](https://redchupa.com/entry/%ed%99%88%ec%96%b4%ec%8b%9c%ec%8a%a4%ed%84%b4%ed%8a%b8ha-%ec%9e%85%eb%ac%b8-%ea%b0%80%ec%9d%b4%eb%93%9c/)** ← 설치부터 첫 자동화까지 단계별 한국어 안내<br/>영문/공식: [HA 공식 설치 가이드](https://www.home-assistant.io/installation/) (Raspberry Pi / Docker / NUC 옵션별)<br/>버전 확인: **설정 → 정보** → **2024.4 이상** 필요 |
| **HACS** (Home Assistant Community Store) | 커뮤니티 통합 설치 도구. 공식 설치 가이드: <https://www.hacs.xyz/docs/use/download/download/> |
| **외부 HTTPS 주소** ⚠️ | 카카오가 로그인 결과를 HA로 보낼 때 필요. 아래 참고 |
| **본인 카카오 계정** | 메시지 받을 카카오톡 계정. 카카오 디벨로퍼스도 같은 계정으로 가입 |

### 외부 HTTPS 주소가 왜 필요한가요?

카카오에서 "로그인 성공!" 결과를 다시 HA에게 알려주려면, **외부 인터넷에서 HA에 접속할 수 있는 https 주소**가 있어야 해요. 없으면 이 통합은 동작 안 합니다.

가장 쉬운 옵션 순서:

| 방법 | 비용 | 난이도 | 추천 대상 |
|---|---|---|---|
| **Nabu Casa Cloud** | 월 $6.5 (≈ 9,000원) | ⭐ 매우 쉬움 | 처음 / 네트워크 어려움 |
| **DuckDNS + Let's Encrypt** | 무료 | ⭐⭐⭐ 보통 | 네트워크 좀 다뤄봤음 |
| **Cloudflare Tunnel** | 무료 | ⭐⭐⭐ 보통 | 도메인 직접 운영 |

> 🌟 **처음이면 Nabu Casa Cloud**: HA → **설정 → Home Assistant Cloud** → 신청.
> 즉시 `https://랜덤이름.ui.nabu.casa` 같은 외부 주소를 받습니다.

본인 HA 외부 주소를 메모해두세요. 3-2 단계에서 한 번 입력해야 합니다.
예: `https://abc12345.ui.nabu.casa` / `https://my-home.duckdns.org`

---

# 1단계 · 카카오 디벨로퍼스에서 앱 만들기

> 💬 카카오 디벨로퍼스가 처음이시죠? 천천히 따라오시면 됩니다.
> 시간: 약 10~15분.

## 1-1. 카카오 디벨로퍼스 가입

1. **<https://developers.kakao.com>** 접속
2. 우상단 **로그인** 버튼 → **카카오 계정으로 로그인**
   - 메시지를 받을 본인 카카오 계정 그대로
3. 첫 가입이면 이용 약관 동의 절차 진행

## 1-2. 새 애플리케이션 만들기

1. 우상단 **"내 애플리케이션"** 클릭
2. **"애플리케이션 추가하기"** 버튼
3. 입력:
   - **앱 이름**: 자유 (예: `HA 카톡 알림`)
   - **사업자명**: 본인 이름 또는 닉네임
   - **카테고리**: 적당히 선택 (예: 라이프스타일)
4. **저장**
5. 방금 만든 앱을 클릭해서 들어가세요

## 1-3. 플랫폼 키 페이지 — 한 곳에서 4가지 설정

좌측 메뉴에서 **"앱 → 플랫폼 키"** 클릭. 그 안에 보이는 **"REST API 키"** 행에 마우스를 올리면 **편집 아이콘** (✏️) 이 나타납니다. 클릭하면 **"REST API 키 수정"** 페이지가 열려요.

> 🎯 **이 한 페이지에서 다음 4가지를 모두** 처리합니다:

### (1) REST API 키 메모하기

페이지 맨 위에 보이는 **REST API 키** (32자리 영문+숫자)
👉 클릭해서 복사 → 메모장에 보관 📌 **나중에 HA에 입력할 첫 번째 값**

### (2) 카카오 로그인 리다이렉트 URI 등록

페이지 중간에 있는 **"카카오 로그인 리다이렉트 URI"** 칸에 **정확히** 다음을 입력:

```
https://my.home-assistant.io/redirect/oauth
```

> 📌 **이 주소를 변형하지 마세요.** 한 글자라도 다르면 나중에 KOE006 에러가 발생합니다.
>
> **이게 뭐죠?** Home Assistant Foundation이 운영하는 표준 OAuth 중계 주소예요.
> 모든 HA 사용자가 공통으로 이 주소를 씁니다. 본인 HA 주소는 카카오에 노출되지 않아요.

### (3) 클라이언트 시크릿 만들기 + 활성화

같은 페이지 아래쪽에서 **"클라이언트 시크릿 → 카카오 로그인"** 섹션을 찾으세요.

> ⚠️ **"비즈니스 인증"** 섹션은 건드리지 마세요. 다른 용도입니다.

1. 코드가 비어 있거나 `-` 라면 **"코드 생성"** 클릭
2. 발급된 32자 코드 **복사해서 메모장에 보관** 📌 **나중에 HA에 입력할 두 번째 값**
3. **"활성화" 토글을 ON** 으로 변경 ⚠️ **이거 빠뜨리면 인증 실패**

### (4) 페이지 하단 [저장] 클릭 💾

⚠️ 입력만 하고 페이지를 떠나면 적용 안 됩니다. **반드시 [저장] 버튼을 누르세요.**

## 1-4. 카카오 로그인 활성화

좌측 메뉴 **"제품 설정 → 카카오 로그인"** 클릭.

- 상단 **"사용 설정"** 토글이 **ON** 인지 확인. (OFF면 ON으로)

## 1-5. talk_message (메시지 전송) 권한 허용

좌측 메뉴 **"제품 설정 → 카카오 로그인 → 동의항목"** 클릭.

스크롤 내려서 **"접근권한"** 표에서 **"카카오톡 메시지 전송 (talk_message)"** 행을 찾으세요.

1. 행의 **"설정"** 버튼 클릭
2. **동의 단계** → **"선택 동의"** 선택
3. **동의 목적**: "카카오톡 메시지 전송" (또는 자유롭게)
4. **저장**

> ⚠️ talk_message 행이 **회색**이라 클릭이 안 되면:
> 좌측 **"앱 → 멤버"** 메뉴에서 본인 카카오 계정을 **팀원으로 추가**하세요.
> 본인에게만 보내는 용도라면 그것만으로 충분합니다.

## ✅ 1단계 완료 체크

| 항목 | OK? |
|---|---|
| REST API 키 메모 | ⬜ |
| 클라이언트 시크릿 코드 메모 | ⬜ |
| 클라이언트 시크릿 "활성화" ON | ⬜ |
| 리다이렉트 URI 등록 + 페이지 [저장] | ⬜ |
| 카카오 로그인 "사용 설정" ON | ⬜ |
| talk_message 동의항목 "선택 동의" 저장 | ⬜ |

전부 ✅ 면 2단계로.

---

# 2단계 · HACS로 컴포넌트 설치

> 💬 HACS는 Home Assistant에 커뮤니티 통합/카드를 설치할 수 있게 해주는 **"앱스토어"** 같은 도구예요.
> 한 번 설치해두면 이후 다른 통합도 쉽게 추가할 수 있어요.

## 2-1. HACS가 이미 설치되어 있나요?

HA 좌측 메뉴에 **HACS** 가 보이면 → 이미 설치됨, **2-2로 건너뛰세요.**

없으면 → **HACS 공식 설치 가이드**: <https://www.hacs.xyz/docs/use/download/download/>
(HA OS / Container / Core / Supervised 각각 절차가 달라요. 본인 HA 설치 방식에 맞춰 따라하세요.
설치 중 GitHub 계정 인증 단계가 있는데, 계정 없으면 무료 가입: <https://github.com/signup>)

설치 끝나고 HA 재시작 후 좌측 메뉴에 **HACS** 가 나타나면 OK.

## 2-2. 이 통합을 HACS에 등록

> 💬 HACS는 **"공식 등록된 통합 카탈로그"** 도 있고, **"개인이 만든 통합"** 도 URL만 알면 가져올 수 있어요.
> 이 통합은 후자 ("사용자 정의 저장소") 로 가져옵니다.

1. HA 좌측 메뉴에서 **HACS** 클릭
2. 우상단 ⋮ (점 세 개) → **"사용자 정의 저장소"** 클릭
3. 입력 창에:
   - **저장소 URL**: `https://github.com/redchupa/kakao-noti`
   - **유형**: `Integration` (통합) 선택
4. **추가**
5. 닫기

## 2-3. 다운로드

1. HACS 메인 화면 → 상단 검색창에 **"Kakao"** 입력
2. **"Kakao Talk (Self Memo) Notify"** 카드가 보이면 클릭
3. 우하단 **"다운로드"** 클릭
4. 버전 선택 화면이 뜨면 최신 버전 그대로 → **"다운로드"**
5. **"Home Assistant 재시작이 필요합니다"** 안내가 보이면 → **설정 → 시스템 → 재시작 → "Home Assistant 다시 시작"**
6. 재시작 후 HA 다시 접속 (1~5분 소요)

---

# 3단계 · HA에서 카카오 연결

## 3-1. Application Credentials 등록 (한 번만)

> 💬 1단계에서 메모한 REST API 키와 Client Secret을 HA에 미리 저장하는 단계입니다.

1. **설정 → 기기 및 서비스** 이동
2. 상단 탭에서 **"애플리케이션 자격 증명"** 클릭 (영어 UI라면 "Application Credentials")
   - 또는 주소창에 직접: `https://<내 HA 주소>/config/application_credentials`
3. 우하단 **"자격 증명 추가"** 버튼
4. 다음과 같이 입력:

   | 항목 | 입력값 |
   |---|---|
   | 통합 | 드롭다운에서 **`Kakao Talk (Self Memo) Notify`** 선택 |
   | 이름 | 아무거나 (예: "내 카카오 앱") |
   | OAuth Client ID | 1-3 (1) 에서 메모한 **REST API 키** 붙여넣기 |
   | OAuth Client Secret | 1-3 (3) 에서 메모한 **클라이언트 시크릿 코드** 붙여넣기 |
5. **추가** 클릭 → 자격 증명 등록 완료

## 3-2. 통합 추가하고 카카오 로그인

1. **설정 → 기기 및 서비스 → 통합 추가** 버튼 (우하단 파란 버튼)
2. 검색창에 **"Kakao"** 입력 → **"Kakao Talk (Self Memo) Notify"** 클릭
3. (위에서 등록한 자격 증명이 자동 선택됨) **다음**
4. 브라우저가 **카카오 로그인 페이지로 자동 이동**
5. **본인 카카오 계정으로 로그인** (자동 로그인 상태면 곧장 다음 단계)
6. 동의 화면이 뜸:
   - **"카카오톡 메시지 전송"** 항목 **체크박스 ✅** 켜기 ⚠️ 빠뜨리면 발송 안 됨
   - **"동의하고 계속하기"** 클릭
7. **"My Home Assistant"** 화면이 한 번 뜹니다:
   - 입력 칸에 **본인 HA의 외부 주소** 입력 (예: `https://abc12345.ui.nabu.casa` 또는 `https://my-home.duckdns.org`)
   - 끝에 `/` 나 `/auth/...` 같은 거 붙이지 마세요. 그냥 베이스 주소만.
   - **Save** 클릭
8. 자동으로 본인 HA로 돌아옴 → 🎉 **"성공" 메시지 + 통합 등록 완료**

> 💡 **7번의 "My Home Assistant" 화면**은 처음 한 번만 뜹니다. 이후엔 브라우저가 기억해서 자동.

---

# 4단계 · 첫 메시지 보내기

테스트로 카톡을 한 번 보내봅시다.

1. HA 좌측 메뉴 → **개발자 도구** → 상단 탭 **서비스** 클릭
2. **서비스** 드롭다운에 `notify.kakao_noti` 검색 → 선택
3. **서비스 데이터** 입력란에 (YAML 모드로 전환):
   ```yaml
   message: "HA에서 보낸 첫 카톡 🎉"
   ```
4. **서비스 호출** 클릭

→ 카카오톡을 열어서 **"나와의 채팅"** 으로 가보세요. 메시지가 도착했으면 성공! 🥳

---

## 실전 사용 예시

### 자동화 1: 현관문 열림 알림

**설정 → 자동화 및 장면 → 자동화 추가** → "Use new automation" → 위 아이콘(⋮) → "YAML 모드로 편집" 후 붙여넣기:

```yaml
alias: 현관문 열림 → 카톡 알림
trigger:
  - platform: state
    entity_id: binary_sensor.front_door
    to: "on"
action:
  - service: notify.kakao_noti
    data:
      message: "현관문 열렸어요 ({{ now().strftime('%H:%M') }})"
```

### 자동화 2: 매일 오전 9시 날씨 요약

```yaml
alias: 오전 브리핑 카톡
trigger:
  - platform: time
    at: "09:00:00"
action:
  - service: notify.kakao_noti
    data:
      title: "오전 브리핑"
      message: |
        🗓 {{ now().strftime('%Y-%m-%d') }}
        🌡 거실 {{ states('sensor.living_room_temperature') }}°C
        ☔ 강수확률 {{ states('sensor.rain_probability') }}%
```

### 자동화 3: HA 재시작 알림

```yaml
alias: HA 시작 알림 카톡
trigger:
  - platform: homeassistant
    event: start
action:
  - delay: "00:00:30"   # 다른 통합도 다 시작될 때까지 30초 여유
  - service: notify.kakao_noti
    data:
      title: "HA 알림"
      message: |
        🏠 Home Assistant 시작됨
        ⏰ {{ now().strftime('%Y-%m-%d %H:%M:%S') }}
```

### 호출 방법 2가지 (어느 쪽이든 OK)

**방식 A — 텔레그램 스타일 (간단)**
```yaml
service: notify.kakao_noti
data:
  message: "..."
```

**방식 B — 엔티티 지정 방식 (멀티 계정 환경에서 유용)**
```yaml
service: notify.send_message
target:
  entity_id: notify.kakao_noti
data:
  message: "..."
```

---

## 가족·여러 명에게 보내기 (멀티 계정)

> 💬 아빠·엄마 카카오톡으로 각자 따로 알림을 받고 싶다면 — 각자 자기 카카오 계정으로 같은 절차를 반복하면 됩니다.

방법 (예: 아빠 + 엄마):

1. **아빠 카카오 계정**: 위 1~3단계를 그대로 따라하면 첫 번째 통합 = `notify.kakao_noti`
2. **엄마 카카오 계정**:
   - 엄마 카카오 계정으로 다시 1단계 (디벨로퍼스 앱 만들기) 부터 진행 (또는 1단계 앱에 엄마를 팀원 추가)
   - HA에서 **3-1 (Application Credentials 등록)** 다시 한 번 (다른 이름으로, 예: "엄마 카카오")
   - HA에서 **3-2 (통합 추가)** 다시 한 번 → 자격 증명 선택 시 엄마 것 선택
   - 카카오 로그인 시 **엄마 카카오 계정으로 로그인**
3. 두 번째 통합이 등록되면 자동으로 `notify.kakao_noti_2` 라는 이름으로 추가됩니다
4. 세 번째는 `notify.kakao_noti_3`, … 자동 번호

> 💡 **같은 카카오 계정을 두 번 등록**하려고 하면 "이미 등록됨"으로 자동 거부됩니다. 안전.

자동화에서:
```yaml
action:
  - service: notify.kakao_noti         # 아빠에게
    data:
      message: "..."
  - service: notify.kakao_noti_2       # 엄마에게
    data:
      message: "..."
```

---

## 토큰은 자동으로 갱신돼요

- 카카오 로그인 토큰은 **6시간**마다 자동 갱신됩니다 (HA가 알아서 처리)
- 갱신 토큰은 **2개월** 동안 유효 — 그 사이에 한 번이라도 메시지를 보내면 자동 연장
- **2개월 동안 한 번도 안 보낸 경우**에만 다시 로그인 필요 — 통합을 삭제하고 위 3-2 단계 다시 진행

---

## 잘 안 될 때

### 통합 추가 단계

| 화면에 뜨는 메시지 | 원인 | 해결 |
|---|---|---|
| **"Application Credentials 등록 필요"** | 3-1 단계 안 함 | 3-1 다시 진행 |
| 카카오 화면에 **"KOE006 앱 관리자 설정 오류"** | 리다이렉트 URI 불일치 | 1-3 (2) 의 URI가 `https://my.home-assistant.io/redirect/oauth` 정확히 일치하는지 확인 + 페이지 하단 [저장] 눌렀는지 확인 |
| **"KOE003"** | 잘못된 REST API 키 | 3-1에 붙여넣은 Client ID 확인 (오타·다른 앱) |
| **"KOE101 앱 권한 없음"** | 카카오 로그인 활성화 OFF | 1-4 단계 확인 |
| 동의 화면에 **"메시지 전송"** 항목이 없음 | talk_message 미설정 또는 회색 | 1-5 단계 확인. 회색이면 팀원 등록 필요 |
| **"Unauthorized"** 류 | Client Secret 불일치 | 1-3 (3) "활성화" ON + 코드 정확히 복사했는지 |

### My Home Assistant 페이지에서

| 증상 | 해결 |
|---|---|
| **"Home Assistant URL 입력"** 화면이 뜸 | 본인 HA 외부 주소 입력 (예: `https://abc.ui.nabu.casa`). 끝에 `/` 붙이지 말 것 |
| Save 눌렀는데 **"연결 안 됨"** | 입력한 주소가 정말 외부에서 접속 가능한지 확인. 다른 네트워크(LTE)에서 그 URL로 HA가 열리는지 |

### 사용 중

| 증상 | 해결 |
|---|---|
| 통합 추가는 됐는데 카톡이 안 옴 | 카카오 로그인 동의 시 "메시지 전송" 체크를 안 함. 통합 삭제 후 3-2 다시 |
| 잘 되다가 갑자기 발송 실패 (401 류) | 2개월 미사용 → 토큰 만료. 통합 삭제 후 3-2 다시 |
| 긴 메시지가 잘림 | 정상 동작 — 1850자 넘으면 자동 절단되고 끝에 `\n… (이하 생략)` 붙음 |

### 자세한 로그 확인

`configuration.yaml` 에 추가 후 HA 재시작:

```yaml
logger:
  default: warning
  logs:
    custom_components.kakao_noti: debug
```

그 후 **설정 → 시스템 → 로그** 에서 `kakao_noti` 검색.

---

## 자주 묻는 질문

**Q. 친구나 가족 카톡으로도 보낼 수 있나요?**
A. 이 통합은 **"나에게 보내기" 만** 지원합니다 (카카오톡 "나와의 채팅"으로만). 친구에게 보내려면 카카오 비즈니스 채널 + 알림톡 같은 별도 유료 서비스가 필요해요. 가족 각자에게 보내는 건 **각자 자기 계정으로 따로 등록** 하면 됩니다 ([멀티 계정](#가족여러-명에게-보내기-멀티-계정) 참고).

**Q. HA 외부 주소가 없으면 절대 안 되나요?**
A. 카카오가 로그인 결과를 HA로 돌려보내는 단계가 있어서 **외부 https 주소가 필요합니다.** Nabu Casa Cloud(월 결제, 가장 쉬움), DuckDNS+Let's Encrypt(무료), Cloudflare Tunnel(무료) 중 하나로 마련하세요.

**Q. 하루에 카톡 몇 개까지 보낼 수 있나요?**
A. 카카오 "나에게 보내기"는 사용자당 **하루 100~500건** (앱 등급에 따라). 일반 자동화에는 충분합니다.

**Q. 카톡 답장으로 HA를 제어할 수 있나요?**
A. 이 통합은 **발송 전용** 입니다. 양방향이 필요하면 텔레그램 봇이 더 좋아요.

**Q. iPhone에서도 카톡으로 받을 수 있나요?**
A. 네 — 카카오톡 앱이 설치된 모든 기기에서 받을 수 있어요 (Android/iOS/PC). HA는 메시지를 카카오 서버로 보내고, 카카오가 본인 모든 기기로 푸시합니다.

**Q. HACS 없이 설치할 수 있나요?**
A. 가능합니다 (수동 복사). 이 저장소의 `custom_components/kakao_noti/` 폴더 전체를 HA의 `config/custom_components/` 안에 복사 후 HA 재시작. 하지만 HACS 쓰면 업데이트가 자동이라 권장합니다.

---

## 후원

이 통합이 유용하셨다면 커피 한 잔 후원 부탁드려요! 🙏

<table>
  <tr>
    <td align="center">
      <b>Toss (토스)</b><br>
      <img src="https://raw.githubusercontent.com/redchupa/kakao-noti/main/images/toss-donation.png" width="200">
    </td>
    <td align="center">
      <b>PayPal</b><br>
      <img src="https://raw.githubusercontent.com/redchupa/kakao-noti/main/images/paypal-donation.png" width="200">
    </td>
  </tr>
</table>

---

## 지원 / 문의

- **이슈 / 버그 제보**: <https://github.com/redchupa/kakao-noti/issues>
- **사용 후기 / 질문**: <https://github.com/redchupa/kakao-noti/discussions>

---

## 라이선스

MIT License — [LICENSE](LICENSE)

---

**도움이 되셨다면 GitHub 저장소에 ⭐ 한 번 부탁드립니다!**
