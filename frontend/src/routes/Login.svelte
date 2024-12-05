<!-- routes/Login.svelte -->
<script>
  import { navigate } from 'svelte-routing';
  import axios from 'axios';
  import { writable } from 'svelte/store';

  let selectedRole = null;
  let inputText = '';
  let errorMessage = '';
  const loading = writable(false);

  async function handleSubmit(event) {
    event.preventDefault();

    const regex = /^\d{5}$/;
    if (!regex.test(inputText)) {
      errorMessage = '유효한 5자리 숫자를 입력하세요.';
      return;
    }

    loading.set(true);
    errorMessage = '';

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
      // 실제 API 호출 (주석 해제)
      // const response = await axios.get(endpoint, { params: { id: inputText } });

      // 임시 조건 (실제 응답 검증으로 대체)
      if (1 == 1) {
        // 역할에 따른 URL로 네비게이션
        navigate(`/${selectedRole}`);
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

  function selectRole(role) {
    selectedRole = role;
    inputText = '';
    errorMessage = '';
  }

  function goHome() {
    navigate('/');
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

  {#if !selectedRole}
    <!-- 홈 페이지: 역할 선택 버튼 -->
    <div>
      <h3>역할을 선택하세요:</h3>
      <button on:click={() => selectRole('pilot')}>파일럿</button>
      <button on:click={() => selectRole('mechanic')}>메카닉</button>
      <button on:click={() => selectRole('customer')}>고객</button>
      <button on:click={() => selectRole('admin')}>관리자</button>
    </div>
  {:else}
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
  {/if}
</div>
