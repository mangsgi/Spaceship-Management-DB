<!-- src/routes/pilot/updateLicense.svelte -->
<script>
  import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정
  import { onMount } from 'svelte';
  import { navigate } from 'svelte-routing';
  import { writable } from 'svelte/store';
  import axios from 'axios';

  let pilotId;
  $: pilotId = $userId;

  let license_number = '';
  let license_expiry_date = '2020-01-01';
  let file; // PDF 파일

  let data_get = []; // 배열로 변경
  const loading = writable(false);
  let errorMessage_get = '';

  async function viewLicense() {
    loading.set(true);
    errorMessage_get = '';

    const endpoint_get = 'http://localhost:8000/licenses'; // 다수 라이센스 반환 API 엔드포인트

    try {
      const response = await axios.get(endpoint_get, { params: { pilot_id: pilotId } });

      if (Array.isArray(response.data)) {
        if (response.data.length > 0) {
          data_get = response.data;
        } else {
          errorMessage_get = '라이센스 정보가 없습니다.';
        }
      } else {
        errorMessage_get = '서버에서 올바른 데이터 형식(배열)을 받지 못했습니다.';
      }
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage_get = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
        } else {
          errorMessage_get = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        errorMessage_get = '서버에 연결할 수 없습니다.';
      }
    } finally {
      loading.set(false);
    }
  }

  async function uploadLicense() {
    const formData = new FormData();

    const licenseData = {
      license_number,
      license_expiry_date,
    };
    formData.append("license_data", new Blob([JSON.stringify(licenseData)], { type: "application/json" }));

    if (file) {
      formData.append("license_file", file);
    } else {
      alert("Choose your file!");
      return;
    }

    try {
      const response = await axios.post(`/pilots/${pilotId}/licenses`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("응답:", response.data);
      alert("업로드 성공!");
      viewLicense(); // 업로드 후 라이센스 정보 갱신
    } catch (error) {
      console.error("업로드 실패:", error.response?.data || error.message);
      alert("업로드에 실패했습니다.");
    }
  }

  function handleFileChange(event) {
    file = event.target.files[0];
  }

  function openPDF(base64PDF) {
    if (!base64PDF) {
      alert("PDF 정보가 없습니다.");
      return;
    }

    const binaryPDF = atob(base64PDF);
    const byteArray = new Uint8Array(binaryPDF.length);
    for (let i = 0; i < binaryPDF.length; i++) {
      byteArray[i] = binaryPDF.charCodeAt(i);
    }
    const blob = new Blob([byteArray], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank'); // 새 탭에서 PDF 열기
  }

  onMount(() => {
    console.log('라이센스 업데이트 컴포넌트가 마운트되었습니다.');
    viewLicense();
  });
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Tinos:ital,wght@0,400;0,700;1,400;1,700&display=swap');

  .pilot-page {
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

  .pilot-container {
    background-color: rgba(0, 0, 0, 0.6);
    padding: 40px;
    border-radius: 20px;
    width: 80%;
    max-width: 800px;
    max-height: 80vh; /* 컨테이너 최대 높이 지정 */
    overflow: auto;   /* 컨테이너 내부 내용이 많을 경우 스크롤 발생 */
}

  h1, h2, h3 {
    font-family: 'Orbitron', sans-serif;
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
    font-family: 'Orbitron', sans-serif;
    font-size: 1em;
  }

  input::placeholder {
    color: #ccc;
  }

  button {
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

  th, td {
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
</style>

<div class="pilot-page">
  <div class="pilot-container">
    <h1>Renew License</h1>
    <p>Pilot ID: {pilotId}</p>
    <button on:click={() => navigate('/pilot')}>Back to Menu
    </button>

    <h2>Upload License</h2>
    <form on:submit|preventDefault={uploadLicense}>
      <label>
        License Number:
        <input type="text" bind:value={license_number} placeholder="License Number" required />
      </label>
      <label>
        License Expiry Date:
        <input type="date" bind:value={license_expiry_date} required />
      </label>
      <label>
        Upload PDF:
        <input type="file" accept="application/pdf" on:change={handleFileChange} required />
      </label>
      <button type="submit">Upload</button>
    </form>

    <h2>Pilot's License Info</h2>
    {#if $loading}
      <p class="loading">Loading...</p>
    {/if}

    {#if errorMessage_get}
      <p class="error">{errorMessage_get}</p>
    {/if}

    {#if data_get.length > 0 && !errorMessage_get}
      <table>
        <thead>
          <tr>
            <th>License ID</th>
            <th>Pilot ID</th>
            <th>License Number</th>
            <th>Expiry Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {#each data_get as license}
            <tr>
              <td>{license.license_id}</td>
              <td>{license.pilot_id}</td>
              <td>{license.license_number}</td>
              <td>{license.license_expiry_date}</td>
              <td>{license.license_status}</td>
              <td><button on:click={() => openPDF(license.license_document)}>View PDF</button></td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </div>
</div>
