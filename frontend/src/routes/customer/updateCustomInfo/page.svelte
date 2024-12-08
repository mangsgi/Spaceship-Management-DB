<script>
  // updatePilotInfo 페이지에 필요한 로직 추가
  import { userId } from "../../../stores.js"; // stores.js의 경로에 따라 조정
  import { onMount } from "svelte";
  import { navigate } from "svelte-routing"; // SvelteKit 사용 시 다른 네비게이션 방식 필요
  import { writable } from "svelte/store";
  import axios from "axios";

  // 반응형 선언으로 userId 값이 변경될 때마다 customerId 업데이트
  $: customerId = $userId;
  const loading = writable(false);
  let errorMessage = "";
  let errorMessage_get = "";
  let data_get = null; // 초기값을 null로 설정

  let name = "";
  let contact_info = "";

  async function findMyInfo() {
    loading.set(true);
    errorMessage_get = "";

    const endpoint_get = "http://localhost:8000/customers";

    try {
      const response = await axios.get(endpoint_get, {
        params: { customer_id: customerId },
      });

      // 응답이 배열인지 확인
      if (Array.isArray(response.data)) {
        const matchedItem = response.data.find(
          (item) => item.customer_id === customerId,
        );
        if (matchedItem) {
          console.log("결과:", matchedItem);
          data_get = matchedItem; // 배열이 아닌 객체로 설정
        } else {
          errorMessage_get = "해당 고객을 찾을 수 없습니다.";
        }
      } else {
        errorMessage_get = "잘못된 응답 형식입니다.";
      }
    } catch (error) {
      console.error("데이터를 가져오는 중 오류 발생:", error);
      if (error.response) {
        // 서버 응답 오류 처리
        if (error.response.status === 400) {
          errorMessage_get = "잘못된 요청입니다. 입력 ID를 확인해주세요.";
        } else {
          errorMessage_get = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        // 요청이 서버에 도달하지 못한 경우
        errorMessage_get = "서버에 연결할 수 없습니다.";
      }
    } finally {
      loading.set(false);
    }
  }

  async function updateMyInfo() {
    loading.set(true);
    errorMessage = "";

    const endpoint = `http://localhost:8000/customers/${customerId}`;

    // 전송할 데이터 정의 (예: 업데이트할 파일럿 정보)
    const payload = {
      name,
      contact_info,
    };

    try {
      const response = await axios.patch(endpoint, payload);

      // 업데이트 성공 시 data_get을 업데이트된 객체로 설정
      if (response.data) {
        data_get = response.data;
        console.log("업데이트 결과:", response.data);
      } else {
        errorMessage = "일치하는 데이터를 찾을 수 없습니다.";
      }
    } catch (error) {
      console.error("데이터 업데이트 중 오류 발생:", error);
      if (error.response) {
        // 서버 응답 오류 처리
        if (error.response.status === 400) {
          errorMessage = "잘못된 요청입니다. 입력 데이터를 확인해주세요.";
        } else if (error.response.status === 422) {
          errorMessage =
            "서버가 요청을 이해했으나 처리할 수 없습니다. 요청 데이터를 확인해주세요.";
        } else if (error.response.status === 404) {
          errorMessage = "해당 파일럿을 찾을 수 없습니다.";
        } else {
          errorMessage = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        // 요청이 서버에 도달하지 못한 경우
        errorMessage = "서버에 연결할 수 없습니다.";
      }
    } finally {
      loading.set(false);
    }
  }

  onMount(() => {
    console.log("컴포넌트가 마운트되었습니다.");
    // 초기화 코드나 데이터 페칭 코드 추가
    findMyInfo();
  });
</script>

<div class="customer-page">
  <div class="customer-container">
  <h2>Update My Info</h2>
  <p>Customer ID: {customerId}</p>
  <button on:click={() => navigate("/customer")}>Back to Menu </button>

  {#if $loading}
    <p class="loading">Loading...</p>
  {/if}

  {#if errorMessage_get}
    <p class="error">{errorMessage_get}</p>
  {/if}

  <!-- 데이터 표시를 위한 테이블 구조 -->
  {#if data_get}
    <form on:submit|preventDefault={updateMyInfo}>
      <h2>Rewrite My Info</h2>
      <input type="text" bind:value={name} placeholder="Name" required />
      <input
        type="text"
        bind:value={contact_info}
        placeholder="Contact Info"
        required
      />
      <button type="submit">Update</button>
    </form>

    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}

    <h3>My info</h3>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Contact Info</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{data_get.name}</td>
          <td>{data_get.contact_info}</td>
        </tr>
      </tbody>
    </table>
  {/if}
</div>
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Tinos:ital,wght@0,400;0,700;1,400;1,700&display=swap");

  .customer-page {
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

.customer-container {
    background-color: rgba(0, 0, 0, 0.6);
    padding: 40px;
    border-radius: 20px;
    width: 80%;
    max-width: 800px;
    max-height: 80vh; /* 컨테이너 최대 높이 지정 */
    overflow: auto;   /* 컨테이너 내부 내용이 많을 경우 스크롤 발생 */
}

  h1,
  h2,
  h3 {
    font-family: "Orbitron", sans-serif;
  }

  h1 {
    font-size: 3em;
    margin-bottom: 20px;
  }

  h2 {
    font-size: 2em;
    margin-bottom: 20px;
  }

  h3 {
    font-size: 1.5em;
    margin-bottom: 20px;
  }

  form {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  label {
    width: 100%;
    margin: 10px 0;
    text-align: left;
    font-size: 1em;
  }

  input[type="text"],
  input[type="date"],
  input[type="file"] {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    border: 2px solid white;
    border-radius: 10px;
    background-color: transparent;
    color: white;
    font-family: "Orbitron", sans-serif;
    font-size: 1em;
  }

  input::placeholder {
    color: #ccc;
  }

  button {
    font-family: "Orbitron", sans-serif;
    font-size: 1em;
    margin: 10px 0;
    padding: 10px 20px;
    border-radius: 50px;
    border: 2px solid white;
    background-color: transparent;
    color: white;
    transition:
      background-color 0.3s,
      color 0.3s;
    width: 100%;
    cursor: pointer;
  }

  button:hover {
    background-color: white;
    color: black;
  }

  table {
    margin: 20px auto;
    border-collapse: collapse;
    width: 100%;
    color: white;
  }

  th,
  td {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: left;
  }

  th {
    background: #333;
  }

  tbody {
    background-color: rgba(0, 0, 0, 0.5); /* White with 80% opacity */
  }

  .loading {
    font-style: italic;
    margin-top: 10px;
  }

  .error {
    color: #ffcccc;
    font-size: 1em;
    margin-top: 10px;
  }

  .home-button {
    width: auto;
    margin: 10px 0;
  }

  .records-section {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  margin-top: 40px;
}

.records-section > div {
  width: 45%;
  min-width: 300px;
}
</style>


<!-- <style>
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
</style> -->
