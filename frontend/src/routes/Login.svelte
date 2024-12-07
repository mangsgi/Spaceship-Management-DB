<!-- routes/Login.svelte -->
<script>
  import { navigate } from 'svelte-routing';
  import axios from 'axios';
  import { writable } from 'svelte/store';
  import { userId } from '../stores.js'; // stores.js의 경로에 따라 조정

  let selectedRole = null;
  let inputText = null;
  let errorMessage = '';
  const loading = writable(false);

  async function handleSubmit(event) {
    event.preventDefault();

    inputText = parseInt(inputText, 10);

    loading.set(true);
    errorMessage = '';

    let endpoint = '';
    let params = {};
    let idKey; // 응답 데이터에서 사용할 ID 키 이름

    switch(selectedRole) {
      case 'pilot':
        endpoint = 'http://localhost:8000/pilots';
        params['pilot_id'] = inputText; // pilot_id로 키 이름 설정
        idKey = 'pilot_id'; // pilot_id로 키 이름 설정
        break;
      case 'mechanic':
        endpoint = 'http://localhost:8000/mechanics';
        params['mechanic_id'] = inputText; // mechanic_id로 키 이름 설정
        idKey = 'mechanic_id'; // mechanic_id로 키 이름 설정
        break;
      case 'customer':
        endpoint = 'http://localhost:8000/customers';
        params['customer_id'] = inputText; // customer_id로 키 이름 설정
        idKey = 'customer_id'; // customer_id로 키 이름 설정
        break;
      case 'admin':
        endpoint = 'http://localhost:8000/admins';
        params['admin_id'] = inputText; // admin_id로 키 이름 설정
        idKey = 'admin_id'; // admin_id로 키 이름 설정
        break;
      default:
        endpoint = 'http://localhost:8000/pilots';
        params['pilot_id'] = inputText; // 기본적으로 pilot_id로 키 이름 설정
        idKey = 'pilot_id'; // 기본적으로 pilot_id로 키 이름 설정
    }

    try {
      const response = await axios.get(endpoint, { params });

      // 임시 조건 (실제 응답 검증으로 대체)
      if (response.data && response.data[idKey] === inputText) {
        // 역할에 따른 URL로 네비게이션
        userId.set(inputText);
        navigate(`/${selectedRole}`);
      } else {
        // 데이터는 있으나 예상된 ID 값이 아니거나 다른 형태의 응답인 경우
        console.log('Received data:', response.data);
        errorMessage = '일치하는 데이터를 찾을 수 없습니다.';
      }
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        // 서버 응답 오류 처리
        if (error.response.status === 400) {
          errorMessage = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
        } else {
          errorMessage = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        // 요청이 서버에 도달하지 못한 경우
        errorMessage = '서버에 연결할 수 없습니다.';
      }
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
          placeholder="본인의 코드를 입력하세요"
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
