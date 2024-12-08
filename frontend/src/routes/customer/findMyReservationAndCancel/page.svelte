<script>
  import { userId } from "../../../stores.js"; // stores.js의 경로에 따라 조정
  import { onMount } from "svelte";
  import { navigate } from "svelte-routing"; // Ensure this is appropriate for your setup
  import { writable } from "svelte/store";
  import axios from "axios";

  // 반응형 선언으로 userId 값이 변경될 때마다 customerId 업데이트
  $: customerId = $userId;

  // 로딩 상태와 에러 메시지 관리
  const loading = writable(false);
  let errorMessage = "";
  let errorMessage_get = "";
  let reservations = []; // 예약 목록을 저장할 배열

  // 예약 성공 메시지
  let successMessage = "";

  // 예약 상태 필터링 변수
  let selectedStatus = "예약"; // 기본값을 '예약'으로 설정

  // 예약 조회 함수
  async function findMyReservation() {
    loading.set(true);
    errorMessage_get = "";
    successMessage = "";

    const endpoint_get = "http://localhost:8000/reservations/my";

    try {
      // 요청 파라미터 설정
      const params = {
        customer_id: customerId,
      };

      if (selectedStatus !== "전체") {
        params.status = selectedStatus;
      }

      const response = await axios.get(endpoint_get, { params });

      // 응답이 배열인지 확인
      if (Array.isArray(response.data)) {
        console.log("예약 목록:", response.data);
        reservations = response.data;
        if (reservations.length === 0) {
          errorMessage_get = "조회된 예약이 없습니다.";
        }
      } else {
        errorMessage_get = "잘못된 응답 형식입니다.";
      }
    } catch (error) {
      console.error("예약 데이터를 가져오는 중 오류 발생:", error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage_get = "잘못된 요청입니다. 입력 ID를 확인해주세요.";
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

  // 예약 취소 함수
  async function cancelReservation(reservationId) {
    loading.set(true);
    errorMessage = "";
    successMessage = "";

    const endpoint = `http://localhost:8000/reservations/my/cancel/${reservationId}`;

    // 전송할 데이터 정의
    const payload = {
      customer_id: customerId, // 'custom_id'에서 'customer_id'로 수정
      // 필요에 따라 추가 필드 삽입
    };

    console.log("Sending payload:", payload); // 페이로드 확인

    try {
      const response = await axios.patch(endpoint, payload);

      if (response.data) {
        console.log("예약 취소 성공:", response.data);
        successMessage = "예약이 성공적으로 취소되었습니다.";
        // 예약 목록을 갱신하기 위해 다시 조회
        findMyReservation();
      } else {
        errorMessage = "예약 취소에 실패했습니다.";
      }
    } catch (error) {
      console.error("예약 취소 중 오류 발생:", error);
      if (error.response) {
        console.error("서버 응답 데이터:", error.response.data);
        if (error.response.status === 400) {
          errorMessage = "잘못된 요청입니다. 입력 데이터를 확인해주세요.";
        } else if (error.response.status === 422) {
          errorMessage =
            error.response.data.message ||
            "요청을 이해했으나 처리할 수 없습니다.";
        } else if (error.response.status === 404) {
          errorMessage = "해당 예약을 찾을 수 없습니다.";
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

  // 컴포넌트가 마운트될 때 예약 조회
  onMount(() => {
    console.log("컴포넌트가 마운트되었습니다.");
    findMyReservation();
  });
</script>

<div class="customer-page">
  <div class="customer-container">
  <h2>My Reservation</h2>
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

  <h2>My Reservation Status</h2>
  <!-- 예약 상태 필터링 섹션 -->
  <div class="filter-section">
    <label for="statusFilter">Reservation Status:</label>
    <select id="statusFilter" bind:value={selectedStatus}>
      <option value="전체">전체</option>
      <option value="예약">예약</option>
      <option value="취소">취소</option>
    </select>
    <button on:click={findMyReservation}>Search</button>
  </div>

  <!-- 예약 목록 표시를 위한 테이블 구조 -->
  {#if reservations.length > 0}
    <h3>My Reservation List</h3>
    <table>
      <thead>
        <tr>
          <th>Reservation ID</th>
          <th>Flight ID</th>
          <th>Reservation Date</th>
          <th>Seat Number</th>
          <th>Status</th>
          <th>Cancel</th>
        </tr>
      </thead>
      <tbody>
        {#each reservations as reservation}
          <tr>
            <td>{reservation.reservation_id}</td>
            <td>{reservation.flight_id}</td>
            <td>{new Date(reservation.reservation_date).toLocaleString()}</td>
            <td>{reservation.seat_number}</td>
            <td>{reservation.status}</td>
            <td>
              {#if reservation.status !== "취소"}
                <button
                  class="cancel-button"
                  on:click={() => {
                    if (confirm("Are you really cancel this reservation?")) {
                      cancelReservation(reservation.reservation_id);
                    }
                  }}
                >
                  Cancel
                </button>
              {:else}
                Canceled
              {/if}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
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
.cancel-button {
    background-color: #ff4d4d;
    color: white;
    border: none;
    padding: 8px 12px;
    cursor: pointer;
    border-radius: 4px;
  }
  .cancel-button:hover {
    background-color: #ff1a1a;
  }
  .filter-section {
    display: flex; /* 요소들을 가로로 정렬 */
    align-items: center; /* 수직 중앙 정렬 */
    gap: 10px; /* 요소 간의 간격 */
    margin-bottom: 20px;
  }
  .filter-section select {
    margin-left: 10px;
    padding: 5px;
    font-size: 1em;
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
    padding: 12px;
  }
  th {
    background-color: #f2f2f2;
  }
  .cancel-button {
    background-color: #ff4d4d;
    color: white;
    border: none;
    padding: 8px 12px;
    cursor: pointer;
    border-radius: 4px;
  }
  .cancel-button:hover {
    background-color: #ff1a1a;
  }
  .filter-section {
    margin-bottom: 20px;
  }
  .filter-section select {
    margin-left: 10px;
    padding: 5px;
    font-size: 1em;
  }
</style> -->
