<script>
  import { createEventDispatcher } from 'svelte';
  import axios from 'axios';
  import { writable } from 'svelte/store';

  const dispatch = createEventDispatcher();

  // 상태 변수
  let currentPage = 'home'; // 'home', 'input', 'pilot', 'mechanic', 'customer', 'admin'
  let selectedRole = null; // 선택된 역할
  let inputText = ''; // 입력된 ID
  let errorMessage = ''; // 에러 메시지
  const loading = writable(false); // 로딩 상태

  // 폼 제출 핸들러
  async function handleSubmit(event) {
    event.preventDefault();

    // 입력 검증: 5자리 숫자인지 확인
    const regex = /^\d{5}$/;
    if (!regex.test(inputText)) {
      errorMessage = '유효한 5자리 숫자를 입력하세요.';
      return;
    }

    // 로딩 상태 시작
    loading.set(true);
    errorMessage = '';

    // 역할에 따른 엔드포인트 설정
    let endpoint = '';
    switch(selectedRole) {
      case 'pilot':
        endpoint = 'https://localhost:8080/pilots/';
        break;
      case 'mechanic':
        endpoint = 'https://localhost:8080/mechanics/';
        break;
      case 'customer':
        endpoint = 'https://localhost:8080/customers/';
        break;
      case 'admin':
        endpoint = 'https://localhost:8080/admins/';
        break;
      default:
        endpoint = 'https://localhost:8080/pilots/';
    }

    try {
      // const response = await axios.get(endpoint, {
      //   params: {
      //     id: inputText
      //   }
      // });

      // 응답 데이터가 존재하고 ID가 일치하는지 확인
      // if (response.data && response.data.id === inputText) {
      if (1 == 1) {
        // 역할에 따른 페이지로 이동
        currentPage = selectedRole;
        // ID와 역할을 유지하기 위해 이벤트로 전달
        dispatch('navigate', { role: selectedRole, id: inputText });
      } else {
        errorMessage = '일치하는 코드가 없습니다.';
      }
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      errorMessage = '데이터를 가져오는 중 오류가 발생했습니다.';
    } finally {
      loading.set(false);
    }
  }

  // 역할 선택 핸들러
  function selectRole(role) {
    selectedRole = role;
    currentPage = 'input';
    inputText = '';
    errorMessage = '';
  }

  // 홈으로 이동하는 함수
  function goHome() {
    currentPage = 'home';
    selectedRole = null;
    inputText = '';
    errorMessage = '';
    dispatch('navigateHome');
  }
</script>

<style>
  .page {
    text-align: center;
    padding: 50px;
  }
  button {
    margin: 5px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 1em;
  }
  input {
    margin: 5px;
    padding: 5px;
    font-size: 1em;
  }
  .error {
    color: red;
  }
  .loading {
    font-style: italic;
  }
</style>

<div class="page">
  <h2>사용자 로그인</h2>
  <button on:click={goHome}>홈으로 이동</button>

  {#if currentPage === 'home'}
    <!-- 홈 페이지: 역할 선택 버튼 -->
    <div>
      <h3>역할을 선택하세요:</h3>
      <button on:click={() => selectRole('pilot')}>파일럿</button>
      <button on:click={() => selectRole('mechanic')}>메카닉</button>
      <button on:click={() => selectRole('customer')}>고객</button>
      <button on:click={() => selectRole('admin')}>관리자</button>
    </div>
  {:else if currentPage === 'input'}
    <!-- ID 입력 페이지 -->
    <div>
      <h3>{selectedRole} ID 입력</h3>
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
        <p class="error">{errorMessage}</p>
      {/if}

      {#if $loading}
        <p class="loading">로딩 중...</p>
      {/if}
    </div>
  {:else if currentPage === 'pilot'}
    <!-- 파일럿 페이지 -->
    <Pilot on:navigateHome={goHome} />
  {:else if currentPage === 'mechanic'}
    <!-- 메카닉 페이지 -->
    <Mechanic on:navigateHome={goHome} />
  {:else if currentPage === 'customer'}
    <!-- 고객 페이지 -->
    <Customer on:navigateHome={goHome} />
  {:else if currentPage === 'admin'}
    <!-- 관리자 페이지 -->
    <Admin on:navigateHome={goHome} />
  {/if}
</div>
