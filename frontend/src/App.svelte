<script>
  import Pilot from './pages/pilot/Pilot.svelte';
  import Mechanic from './pages/mechanic/Mechanic.svelte';
  import Customer from './pages/customer/Customer.svelte';
  import Admin from './pages/admin/Admin.svelte';

  // 상태 변수
  let currentPage = 'home'; // 'home', 'pilot', 'mechanic', 'customer', 'admin'
  let selectedButton = null; // 클릭된 버튼 번호 (1, 2, 3, 4)
  let showInput = false; // 입력창 표시 여부
  let inputText = ''; // 입력된 텍스트
  let errorMessage = ''; // 오류 메시지

  // 버튼 클릭 핸들러
  function handleButtonClick(buttonId) {
    selectedButton = buttonId;
    showInput = true;
    errorMessage = '';
    inputText = '';
  }

  // 폼 제출 핸들러
  async function handleSubmit(event) {
    event.preventDefault();

    // 입력 검증: 5자리 숫자인지 확인
    const regex = /^\d{5}$/;
    if (!regex.test(inputText)) {
      errorMessage = '유효한 5자리 숫자를 입력하세요.';
      return;
    }

    try {
      // 백엔드 API로 POST 요청 전송(막기)
      
      // const response = await fetch('https://your-backend-api.com/endpoint', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json'
      //   },
      //   body: JSON.stringify({ code: inputText })
      // });

      // if (!response.ok) {
      //   throw new Error('네트워크 응답이 정상적이지 않습니다.');
      // }

      // const data = await response.json();
      
      // 백엔드에서 `matched` 필드로 일치 여부 반환한다고 가정
      // if (data.matched) {
      if (1 == 1) {
        // 선택된 버튼에 따라 해당 페이지로 네비게이션
        currentPage = selectedButton === 1 ? 'pilot' :
                      selectedButton === 2 ? 'mechanic' :
                      selectedButton === 3 ? 'customer' :
                      'admin';
        // 상태 초기화
        showInput = false;
        selectedButton = null;
      } else {
        errorMessage = '일치하는 코드가 없습니다.';
      }
    } catch (error) {
      console.error('오류:', error);
      errorMessage = '요청 처리 중 오류가 발생했습니다.';
    }
  }

  // 홈으로 네비게이트하는 함수
  function navigateHome() {
    currentPage = 'home';
    selectedButton = null;
    showInput = false;
    inputText = '';
    errorMessage = '';
  }
</script>

<style>
  .button-container {
    display: flex;
    gap: 10px;
    margin: 20px 0;
    justify-content: center;
  }
  button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
  }
  .input-container {
    margin-top: 20px;
    text-align: center;
  }
  .input-container input {
    padding: 8px;
    font-size: 16px;
    width: 200px;
  }
  .input-container button {
    padding: 8px 16px;
    font-size: 16px;
    margin-left: 10px;
    cursor: pointer;
  }
  .error {
    color: red;
    margin-top: 10px;
  }
  .home, .page {
    text-align: center;
    padding: 50px;
  }
</style>

{#if currentPage === 'home'}
  <div class="home">
    <h1>홈 화면</h1>
    <div class="button-container">
      <button on:click={() => handleButtonClick(1)}>PILOT</button>
      <button on:click={() => handleButtonClick(2)}>MECHANIC</button>
      <button on:click={() => handleButtonClick(3)}>CUSTOMER</button>
      <button on:click={() => handleButtonClick(4)}>ADMIN</button>
    </div>

    {#if showInput}
      <div class="input-container">
        <form on:submit|preventDefault={handleSubmit}>
          <input
            type="text"
            bind:value={inputText}
            placeholder="5자리 코드를 입력하세요"
            maxlength="5"
            required
          />
          <button type="submit">제출</button>
        </form>
        {#if errorMessage}
          <div class="error">{errorMessage}</div>
        {/if}
      </div>
    {/if}
  </div>
{:else if currentPage === 'pilot'}
  <Pilot on:navigateHome={navigateHome} />
{:else if currentPage === 'mechanic'}
  <Mechanic on:navigateHome={navigateHome} />
{:else if currentPage === 'customer'}
  <Customer on:navigateHome={navigateHome} />
{:else if currentPage === 'admin'}
  <Admin on:navigateHome={navigateHome} />
{/if}
