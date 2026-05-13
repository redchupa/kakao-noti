<p align="center">
  <img src="https://raw.githubusercontent.com/redchupa/kakao-noti/main/images/logo.png" alt="Kakao Notify Logo" width="640">
</p>

<p align="center">
  <a href="https://github.com/hacs/integration"><img src="https://img.shields.io/badge/HACS-Custom-41BDF5.svg" alt="HACS"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/redchupa/kakao-noti" alt="License"></a>
  <a href="https://github.com/redchupa/kakao-noti/stargazers"><img src="https://img.shields.io/github/stars/redchupa/kakao-noti?style=social" alt="Stars"></a>
</p>

# 카카오톡 나에게 보내기 (Home Assistant)

Home Assistant에서 일어나는 일을 **내 카카오톡 "나와의 채팅"** 으로 받아보세요.
텔레그램 알림처럼 자동화·스크립트 어디서든 한 줄로 호출할 수 있습니다.

```yaml
service: notify.kakao_noti
data:
  message: "현관문이 열렸어요"
```

---

## 이걸로 뭘 할 수 있나요?

- 🏠 현관문 열림, 누수 감지, 가스 차단 같은 **집안 상태 알림**
- 🌧️ 일정 시간이 되면 **오늘 날씨/일정 요약** 발송
- 📊 가전·전기 사용량 일일 리포트
- 🚨 카메라 모션 감지 시 즉시 알림

…요컨대 **텔레그램 봇으로 받던 알림을 카톡으로 받게** 만들어줍니다.

---

## 시작하기 전 준비물

- [x] 메시지를 받을 본인 **카카오 계정** (카카오톡 "나와의 채팅"으로 도착함)
- [x] Home Assistant **2024.4 이상**
- [x] HA가 **외부에서 https로 접근 가능**해야 합니다
  - Nabu Casa Cloud, DuckDNS+Let's Encrypt, Cloudflare Tunnel 등 어떤 방식이든 OK
  - 카카오가 로그인 결과를 내 HA로 돌려보낼 때 필요합니다
  - 외부 URL을 모르겠다면 HA에서 **설정 → 시스템 → 네트워크 → "Home Assistant URL"** 확인

준비됐다면 단계 1부터 시작하세요. 총 15~20분 소요.

---

# 1단계 · 카카오에서 앱 만들기

> 한 번만 하면 되는 작업입니다. 이미 카카오 앱이 있다면 [2단계](#2단계--앱-설정하기)로.

1. **<https://developers.kakao.com>** 접속
2. **메시지 받을 본인 카카오 계정으로 로그인** (다른 계정으로 만들면 본인에게 도착 안 함)
3. 우상단 **"내 애플리케이션"** 클릭
4. **"애플리케이션 추가하기"** 버튼
5. 앱 이름·사업자명·카테고리 적당히 입력 → 저장
   - 앱 이름은 자유 (예: `HA-카톡알림`)
   - 사업자명은 본인 이름이나 닉네임으로 OK
6. 만든 앱을 클릭해서 들어가세요

---

# 2단계 · 앱 설정하기

> 카카오 콘솔에서 다음 설정을 마칩니다. 빠뜨리면 나중에 카톡이 안 와요.
>
> **카카오 콘솔 좌측 메뉴 구조 미리보기**:
> ```
> 앱 설정
>   └ 대시보드
> 앱
>   ├ 일반
>   ├ 플랫폼 키       ← 2-1 ~ 2-3 여기에서 모두 처리
>   ├ 어드민 키
>   ├ 멤버           ← 2-6 (필요 시) 여기서 팀원 추가
>   └ ...
> 제품 설정
>   └ 카카오 로그인   ← 2-4, 2-5 여기서 처리
> ```

## 2-1 ~ 2-3. 플랫폼 키 페이지에서 한 번에 처리

좌측 메뉴 **"앱 → 플랫폼 키"** 클릭 → **REST API 키** 행 옆의 **편집 아이콘** 클릭
(또는 키 값을 클릭) → **"REST API 키 수정"** 페이지 진입.

이 한 페이지에서 다음 세 가지를 모두 합니다.

### 2-1. REST API 키 복사 ✏️

페이지 상단 **REST API 키** (32자 hex) 복사 → 메모장에 보관.
📌 **HA에서 입력할 첫 번째 값** (Client ID 자리).

### 2-2. 카카오 로그인 리다이렉트 URI 등록 🌐

페이지 중간 **"카카오 로그인 리다이렉트 URI"** 칸에 다음을 정확히 입력:

```
https://my.home-assistant.io/redirect/oauth
```

> 💡 이 주소는 Home Assistant Foundation이 제공하는 **OAuth 중간 redirector**입니다.
> 카카오 로그인 결과가 이 주소로 도착하면 내 HA로 자동 안전하게 전달됩니다.
> 모든 HA 사용자에게 동일한 주소를 쓰면 되고, 본인 HA URL을 카카오에 노출할 필요 없습니다.

> ⚠️ 주소를 **변형하지 마세요** — `my.home-assistant.io/redirect/oauth` 정확히 그대로.
> 한 글자라도 다르면 `KOE006 앱 관리자 설정 오류` 발생.

### 2-3. 클라이언트 시크릿 생성 + 활성화 🔐

같은 페이지 아래쪽 **"클라이언트 시크릿 → 카카오 로그인"** 섹션 (⚠️ **"비즈니스 인증" 아님**):

1. 코드가 `-` 이면 **"코드 생성"** 클릭
2. 발급된 32자 코드 **복사해서 메모장에 보관** 📌 **HA에서 입력할 두 번째 값** (Client Secret 자리)
3. **"활성화" 토글 → ON** ⚠️ **이 토글 꼭 켜기**

### 2-1~2-3 마무리: 페이지 하단 [저장] 버튼 클릭 💾

⚠️ **반드시 페이지 하단의 [저장] 버튼**까지 눌러야 위 내용이 반영됩니다.
입력만 하고 페이지를 떠나면 저장 안 됩니다.

---

## 2-4. 카카오 로그인 사용 설정

좌측 메뉴 **"제품 설정 → 카카오 로그인"** 클릭:

- 상단 **"사용 설정"** 토글 → **ON**

(꺼져 있으면 OAuth 시 `KOE101` 에러)

## 2-5. 메시지 보내기 권한 (talk_message) 켜기

좌측 메뉴 **"제품 설정 → 카카오 로그인 → 동의항목"** (또는 카카오 로그인 페이지 내 "동의항목" 탭):

1. 표 아래쪽 **"접근권한"** 영역에서 **"카카오톡 메시지 전송 (talk_message)"** 행을 찾기
2. 행의 **"설정"** 버튼 클릭
3. **동의 단계**: **"선택 동의"** 선택
4. **동의 목적**: "카카오톡 메시지 전송" (또는 자유)
5. 저장

> ⚠️ **talk_message 행이 회색**이라 클릭이 안 되면:
> 좌측 **"앱 → 멤버"** (또는 "내 애플리케이션 → 팀 관리") 에서
> **본인 카카오 계정**을 팀원으로 추가하세요.
> 본인에게만 보내는 용도는 그것만으로 충분합니다.

---

## ✅ 카카오 설정 완료 체크리스트

플랫폼 키 페이지 (2-1~2-3 한 번에):

| 항목 | 확인 |
|---|---|
| REST API 키 메모해뒀나요? | ⬜ |
| Redirect URI에 `https://my.home-assistant.io/redirect/oauth` 등록? | ⬜ |
| 클라이언트 시크릿 코드 메모해뒀나요? | ⬜ |
| 클라이언트 시크릿 "활성화" 토글 ON? | ⬜ |
| 페이지 하단 [저장] 버튼 눌렀나요? ⚠️ | ⬜ |

카카오 로그인 페이지:

| 항목 | 확인 |
|---|---|
| "사용 설정" 토글 ON? | ⬜ |
| talk_message 동의항목 "선택 동의" 저장? | ⬜ |

전부 ✅ 면 다음 단계로.

---

# 3단계 · Home Assistant에 컴포넌트 설치

## 방법 A · HACS로 (권장)

1. HACS → 우상단 ⋮ → **"사용자 정의 저장소"** 클릭
2. 이 GitHub 저장소 URL 추가, 카테고리 = **Integration**
3. "Kakao Talk (Self Memo) Notify" 검색 → 다운로드
4. **Home Assistant 재시작** (설정 → 시스템 → 재시작 → "Home Assistant 다시 시작")

## 방법 B · 수동 설치

1. GitHub에서 이 저장소를 다운로드 (Code → Download ZIP)
2. 압축 풀고 `custom_components/kakao_noti/` 폴더 전체를 HA의
   **`config/custom_components/`** 안에 복사
3. **Home Assistant 재시작**

---

# 4단계 · HA에서 카카오 연결

## 4-1. 자격 증명 등록 (한 번만)

1. **설정 → 기기 및 서비스** → 상단 탭에서 **"애플리케이션 자격 증명"** (Application Credentials) 클릭
2. 우하단 **"자격 증명 추가"** 버튼
3. 입력:

   | 항목 | 입력값 |
   |---|---|
   | 통합 | `Kakao Talk (Self Memo) Notify` 선택 |
   | 이름 | 아무거나 (예: "내 카카오 앱") |
   | OAuth Client ID | 2-1에서 메모한 **REST API 키** |
   | OAuth Client Secret | 2-2에서 메모한 **클라이언트 시크릿 코드** |
4. **추가**

## 4-2. 통합 추가하고 인증

1. **설정 → 기기 및 서비스 → 통합 추가**
2. **"Kakao"** 검색 → **"Kakao Talk (Self Memo) Notify"** 클릭
3. (자격 증명이 자동 선택됨) **다음**
4. **브라우저가 카카오 로그인 페이지로 자동 이동** 합니다
5. 카카오 로그인 → 동의 화면에서 **"카카오톡 메시지 전송" 체크박스 ✅** → **"동의하고 계속하기"**
6. (처음 한 번만) `my.home-assistant.io` 페이지가 본인 HA 주소를 묻습니다 → 외부 URL 입력 (예: `https://ha.example.com`) → **Save**
7. 자동으로 HA로 복귀 → 🎉 **통합 등록 완료**

> 💡 옵션 입력 화면 없음 — 인증 끝나면 곧바로 사용할 수 있어요.
> 알림 서비스 이름은 **`notify.kakao_noti`** 로 자동 등록됩니다.

## 4-3. 첫 메시지 보내기

**개발자 도구 → 서비스** 로 이동:

- 서비스: `notify.kakao_noti`
- 데이터:
  ```yaml
  message: "HA에서 보낸 첫 카톡! 🎉"
  ```
- **서비스 호출** 버튼

→ 카카오톡 **"나와의 채팅"** 에 메시지가 도착하면 성공입니다.

---

# 사용법

## 자동화에서

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

## 제목 + 본문

```yaml
service: notify.kakao_noti
data:
  title: "온도 경보"
  message: "거실 {{ states('sensor.living_temp') }}°C"
```
→ 카톡에는 `[온도 경보]\n거실 28°C` 형식으로 도착.

## 여러 줄 메시지 (요약 리포트)

```yaml
service: notify.kakao_noti
data:
  message: |
    📊 오늘의 요약
    🌡️ 거실 {{ states('sensor.living_temp') }}°C
    💧 습도 {{ states('sensor.living_humidity') }}%
    ⚡ 사용량 {{ states('sensor.daily_power') }} kWh
```

## 호출 방법 두 가지 (둘 다 작동, 편한 쪽 사용)

**방식 1 — 텔레그램 스타일 (간단)**
```yaml
service: notify.kakao_noti
data:
  message: "..."
```

**방식 2 — 엔티티 지정 방식**
```yaml
service: notify.send_message
target:
  entity_id: notify.kakao_noti
data:
  message: "..."
```

---

# 토큰은 알아서 갱신돼요

- 카카오 로그인 토큰은 **6시간**마다 자동 갱신됩니다 (HA가 처리)
- 갱신 토큰은 **2개월** 동안 유효 — 그 사이에 한 번이라도 메시지를 보내면 자동 연장됩니다
- **2개월 동안 한 번도 안 보낸 경우**에만 다시 로그인 필요 — 통합을 삭제 후 4-2 단계 다시 진행

---

# 잘 안 될 때

## 통합 추가 단계에서

| 화면에 뜨는 메시지 | 원인 | 해결 |
|---|---|---|
| "Application Credentials 등록 필요" | 자격 증명 미등록 | 위 **4-1단계** 진행 |
| 카카오 화면에서 **KOE006** | Redirect URI 불일치 | 카카오 콘솔에 등록한 주소가 HA URL과 한 글자라도 다른지 확인. `/auth/external/callback` 까지 정확히 |
| 카카오 화면에서 **KOE003** | 잘못된 REST API 키 | 자격 증명에 입력한 Client ID 확인 |
| 카카오 화면에서 **KOE101** | 카카오 로그인 활성화 OFF | **2-4단계** 확인 |
| 동의 화면에 "메시지 전송" 항목이 안 보임 | talk_message 설정 안 됨 | **2-5단계** 다시 |
| "Unauthorized" 류 메시지 | 클라이언트 시크릿 불일치 | 토글 ON인지 + 코드 정확히 복사했는지 확인 |

## 메시지가 안 올 때

| 증상 | 해결 |
|---|---|
| 통합 추가는 성공인데 카톡 안 옴 | 카카오 로그인 동의 시 "메시지 전송" 체크 안 함 → 통합 삭제 후 재추가하며 체크 확인 |
| 잘 되다가 갑자기 401 에러 반복 | 2개월 미사용으로 갱신 토큰 만료 → 통합 삭제 후 재추가 (4-2단계 다시) |
| 긴 메시지가 잘림 | 정상 동작 — 1850자 넘으면 자동 절단되고 끝에 `\n… (이하 생략)` 붙음 |

## 자세한 로그 보기

`configuration.yaml` 에 추가하고 HA 재시작:

```yaml
logger:
  default: warning
  logs:
    custom_components.kakao_noti: debug
```

**설정 → 시스템 → 로그** 에서 `kakao_noti` 검색.

---

# 자주 묻는 질문

**Q. 친구나 가족에게도 보낼 수 있나요?**
A. 이 통합은 **"나에게 보내기"** 만 지원합니다. 본인 카카오톡 "나와의 채팅"으로만 도착해요.
다른 사람에게 보내려면 카카오 비즈니스 채널 + 알림톡 같은 별도 서비스가 필요합니다.

**Q. HA가 외부에서 접속 안 되는 환경인데도 가능한가요?**
A. 카카오가 로그인 결과를 HA로 돌려줘야 해서 **외부 HTTPS 접속이 필수**입니다.
Nabu Casa Cloud(월 결제), DuckDNS+Let's Encrypt(무료), Cloudflare Tunnel(무료) 중 편한 방식으로 외부 URL 마련하세요.

**Q. 여러 명에게 각자 자기 카톡으로 알림 보내고 싶어요.**
A. 가능합니다 — **통합 추가를 반복**하면 됩니다.
1. 가족 구성원이 각자 본인 카카오 계정으로 1~2단계를 따라 카카오 앱을 만들어요. (또는 한 앱에 팀원으로 추가)
2. HA의 **설정 → 기기 및 서비스 → "Application Credentials"** 에서 각 앱의 자격 증명을 추가 등록
3. **통합 추가** 를 사람 수만큼 반복 — 그때마다 다른 카카오 계정으로 로그인
4. 첫 번째 등록은 `notify.kakao_noti`, 두 번째는 `notify.kakao_noti_2`, 세 번째는 `notify.kakao_noti_3` … 자동 번호 부여 됨
5. 같은 카카오 계정을 두 번 등록하려고 하면 "이미 등록됨"으로 자동 거부 (안전)

**Q. 하루에 몇 개까지 보낼 수 있나요?**
A. 카카오 "나에게 보내기"는 사용자당 **하루 100~500건** (앱 등급에 따라 다름).
일반 자동화 용도엔 충분합니다.

**Q. 카톡으로 답장도 받을 수 있나요?**
A. 이 통합은 발송 전용입니다. 양방향이 필요하다면 카카오 챗봇 빌더 같은 별도 서비스가 필요합니다.

---

## 후원

이 통합이 유용하셨다면 커피 한 잔 후원 부탁드립니다! 🙏

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

- **Issues**: <https://github.com/redchupa/kakao-noti/issues>
- **Discussions**: <https://github.com/redchupa/kakao-noti/discussions>

---

## 라이선스

MIT License — [LICENSE](LICENSE)

---

**문제가 생기거나 개선 아이디어 있으면 GitHub 이슈로 알려주세요. 잘 쓰시면 ⭐ 부탁드립니다!**
