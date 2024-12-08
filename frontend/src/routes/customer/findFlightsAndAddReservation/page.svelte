<script>
  import { userId } from "../../../stores.js"; // stores.js의 경로에 따라 조정
  import { onMount } from "svelte";
  import { navigate } from "svelte-routing"; // SvelteKit 사용 시 다른 네비게이션 방식 필요
  import { writable } from "svelte/store";
  import axios from "axios";

  // 반응형 선언으로 userId 값이 변경될 때마다 customerId 업데이트
  $: customerId = $userId;

  // 로딩 상태와 에러 메시지 관리
  const loading = writable(false);
  let errorMessage = "";
  let errorMessage_get = "";

  // 비행 필터링 파라미터
  let departure_location = "";
  let arrival_location = "";
  let departure_date = "";
  let sort_by = "";

  // 비행 목록 저장 변수
  let flightData = [];

  // 예약할 비행 선택 변수
  let selectedFlightId = null;

  // 예약 성공 메시지
  let successMessage = "";

  // 비행 일정 필터링 함수
  async function findCustomFlight() {
    loading.set(true);
    errorMessage_get = "";
    successMessage = "";

    const endpoint_get = "http://localhost:8000/flights_by_customer";

    try {
      const response = await axios.get(endpoint_get, {
        params: {
          departure_location,
          arrival_location,
          departure_date,
          sort_by,
        },
      });

      // 응답이 배열인지 확인
      if (Array.isArray(response.data)) {
        console.log("Flights:", response.data);
        flightData = response.data;
        if (flightData.length === 0) {
          errorMessage_get = "검색 결과가 없습니다.";
        }
      } else {
        errorMessage_get = "잘못된 응답 형식입니다.";
      }
    } catch (error) {
      console.error("비행 데이터를 가져오는 중 오류 발생:", error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage_get = "잘못된 요청입니다. 입력을 확인해주세요.";
        } else {
          errorMessage_get = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        errorMessage_get = "서버에 연결할 수 없습니다.";
      }
    } finally {
      loading.set(false);
    }
  }

  // 예약 생성 함수
  async function addReservation() {
    if (!selectedFlightId) {
      errorMessage = "예약할 비행을 선택해주세요.";
      return;
    }

    loading.set(true);
    errorMessage = "";
    successMessage = "";

    const endpoint = `http://localhost:8000/reservations`;

    // 전송할 데이터 정의
    const payload = {
      customer_id: customerId,
      flight_id: selectedFlightId,
      seat_number: "A08",
      // 필요에 따라 추가 필드 삽입
    };

    try {
      const response = await axios.post(endpoint, payload);

      if (response.data) {
        console.log("예약 생성 성공:", response.data);
        successMessage = "예약이 성공적으로 생성되었습니다.";
        // 예약 후 선택 초기화
        selectedFlightId = null;
        // 필요 시 예약 내역을 불러오는 함수 호출
      } else {
        errorMessage = "예약 생성에 실패했습니다.";
      }
    } catch (error) {
      console.error("예약 생성 중 오류 발생:", error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage = "잘못된 요청입니다. 입력 데이터를 확인해주세요.";
        } else if (error.response.status === 422) {
          errorMessage = "요청을 이해했으나 처리할 수 없습니다.";
        } else if (error.response.status === 404) {
          errorMessage = "해당 비행을 찾을 수 없습니다.";
        } else {
          errorMessage = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        errorMessage = "서버에 연결할 수 없습니다.";
      }
    } finally {
      loading.set(false);
    }
  }

  // 컴포넌트가 마운트될 때 초기화
  onMount(() => {
    console.log("컴포넌트가 마운트되었습니다.");
    // 필요 시 초기 비행 목록을 불러오려면 findCustomFlight() 호출
  });
</script>

<div class="customer-page">
  <div class="customer-container">
  <h2>Flight Reservation</h2>
  <p>Customer ID: {customerId}</p>
  <button on:click={() => navigate("/customer")}>Back to Menu </button>

  {#if $loading}
    <p class="loading">Loading...</p>
  {/if}

  {#if errorMessage_get}
    <p class="error">{errorMessage_get}</p>
  {/if}

  {#if successMessage}
    <p class="success">{successMessage}</p>
  {/if}

  <h3>Flights Filter</h3>
  <form on:submit|preventDefault={findCustomFlight}>
    <input type="text" bind:value={departure_location} placeholder="Departure Location" />
    <input type="text" bind:value={arrival_location} placeholder="Arrival Location" />
    <input type="date" bind:value={departure_date} placeholder="Departure Date" />
    <select bind:value={sort_by}>
      <option value="">Select Sorting</option>
      <option value="departure_time">Departure Time</option>
      <option value="arrival_time">Arrival Time</option>
      <!-- 필요에 따라 추가 정렬 옵션 삽입 -->
    </select>
    <button type="submit">Search Flights</button>
  </form>

  {#if flightData.length > 0}
    <h3>Searched Flight</h3>
    <table>
      <thead>
        <tr>
          <th>Flight ID</th>
          <th>Departure Location</th>
          <th>Arrival Location</th>
          <th>Departure Time</th>
          <th>Arrival Time</th>
          <th>Choose</th>
        </tr>
      </thead>
      <tbody>
        {#each flightData as flight}
          <tr>
            <td>{flight.flight_id}</td>
            <td>{flight.departure_location}</td>
            <td>{flight.arrival_location}</td>
            <td>{new Date(flight.departure_time).toLocaleString()}</td>
            <td>{new Date(flight.arrival_time).toLocaleString()}</td>
            <td>
              <input
                type="radio"
                name="selectedFlight"
                bind:group={selectedFlightId}
                value={flight.flight_id}
              />
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
    <button on:click={addReservation}>Reservation</button>
  {/if}

  {#if errorMessage}
    <p class="error">{errorMessage}</p>
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
  input,
  select {
    margin: 5px;
    padding: 5px;
    font-size: 1em;
  }
  .error {
    color: red;
  }
  .success {
    color: green;
  }
  .loading {
    font-style: italic;
  }
  table {
    margin: 20px auto;
    border-collapse: collapse;
    width: 90%;
  }
  th,
  td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  th {
    background-color: #f2f2f2;
  }
</style> -->
