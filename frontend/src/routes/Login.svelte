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
    let idKey;

    switch(selectedRole) {
      case 'pilot':
        endpoint = 'http://localhost:8000/pilots';
        params['pilot_id'] = inputText;
        idKey = 'pilot_id';
        break;
      case 'mechanic':
        endpoint = 'http://localhost:8000/mechanics';
        params['mechanic_id'] = inputText;
        idKey = 'mechanic_id';
        break;
      case 'customer':
        endpoint = 'http://localhost:8000/customers';
        params['customer_id'] = inputText;
        idKey = 'customer_id';
        break;
      case 'admin':
        endpoint = 'http://localhost:8000/administrators';
        params['admin_id'] = inputText;
        idKey = 'admin_id';
        break;
      default:
        endpoint = 'http://localhost:8000/pilots';
        params['pilot_id'] = inputText;
        idKey = 'pilot_id';
    }

    try {
      const response = await axios.get(endpoint, { params });

      if (Array.isArray(response.data)) {
        const matchedItem = response.data.find(item => item[idKey] === inputText);

        if (matchedItem) {
          userId.set(inputText);
          navigate(`/${selectedRole}`);
        } else {
          console.log('Received data:', response.data);
          errorMessage = '일치하는 데이터를 찾을 수 없습니다.';
        }
      } else {
        console.log('Unexpected data format:', response.data);
        errorMessage = '데이터 형식이 예상과 다릅니다.';
      }
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
        } else {
          errorMessage = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
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
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Tinos:ital,wght@0,400;0,700;1,400;1,700&display=swap');

  .login-page {
  position: absolute; /* 또는 fixed */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  
  text-align: center;
  padding: 0; /* 패딩 제거 */
  background-image: url('/images/space_main.png'); /* 원하는 배경 이미지 경로 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat; /* 배경 이미지 반복 방지 */
  background-attachment: fixed; /* 배경 이미지 고정 */
  color: white;
  width: 100vw; /* 전체 뷰포트 너비의 120% */
  height: 120vh; /* 전체 뷰포트 높이의 120% */
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-family: 'Orbitron', sans-serif;
  overflow: hidden; /* 필요에 따라 추가 */
}


.login-container {
    background-color: rgba(53, 53, 53, 0.4);
    padding: 40px;
    border-radius: 20px;
    width: 80%;
    max-width: 800px;
    max-height: 80vh; /* 컨테이너 최대 높이 지정 */
    overflow: auto;   /* 컨테이너 내부 내용이 많을 경우 스크롤 발생 */
}

  h1{
    font-family: 'Orbitron', sans-serif;
    font-size: 3em;
  }

  h2 {
    font-family: 'Orbitron', sans-serif;
    font-size: 2em;
    margin-bottom: 20px;
  }

  h3 {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.5em;
    margin-bottom: 20px;
  }

  button, input {
    font-family: 'Orbitron', sans-serif;
    font-size: 1em;
    margin: 10px 0;
    padding: 10px 20px;
    border-radius: 50px;
    border: 2px solid white;
    background-color: transparent;
    color: white;
    transition: background-color 0.3s, color 0.3s;
    width: 100%;
  }

  button:hover {
    background-color: white;
    color: black;
  }

  input {
    border: 2px solid white;
    text-align: center;
  }

  .error {
    color: #ffcccc;
    font-size: 0.9em;
    margin-top: 10px;
  }

  .loading {
    font-style: italic;
    margin-top: 10px;
  }

  .role-buttons button {
    width: auto;
    margin: 5px;
  }
  .home-button{
    width: auto;
    margin: 5px;
  }
</style>

<div class="login-page">
  <div class="login-container">
  
    <h2>User Login</h2>
    <button on:click={goHome} class="home-button">Main Page</button>

    {#if !selectedRole}
      <!-- 역할 선택 -->
      <h3>Select Your Role</h3>
      <div class="role-buttons">
        <button on:click={() => selectRole('pilot')}>Pilot</button>
        <button on:click={() => selectRole('mechanic')}>Mechanic</button>
        <button on:click={() => selectRole('customer')}>Customer</button>
        <button on:click={() => selectRole('admin')}>Admin</button>
      </div>
    {:else}
      <!-- ID 입력 -->
      <h3>Write Your {selectedRole} ID</h3>
      <form on:submit|preventDefault={handleSubmit}>
        <input
          class="input_code"
          type="text"
          bind:value={inputText}
          placeholder="Write your ID"
          maxlength="5"
          required
        />
        <button type="submit">Submit</button>
      </form>

      {#if errorMessage}
        <p class="error">{errorMessage}</p>
      {/if}

      {#if $loading}
        <p class="loading">로딩 중...</p>
      {/if}
    {/if}
  </div>
</div>
