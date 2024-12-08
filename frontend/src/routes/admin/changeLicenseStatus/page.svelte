<script>
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정
  import axios from 'axios';

  // 상태 관리
  const loading = writable(false);
  let errorMessage_get = '';
  let errorMessage_upload = '';
  
  // 사용자 ID 구독
  let adminId;
  $: adminId = $userId;

  // 라이센스 관련 변수
  let file; // PDF 파일

  let data_get = []; // 배열로 변경

  // 라이센스 조회 함수
  async function viewLicense() {
    loading.set(true);
    errorMessage_get = '';

    const endpoint_get = 'http://localhost:8000/licenses'; // 라이센스 조회 API 엔드포인트

    try {
      const response = await axios.get(endpoint_get);

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

  // 라이센스 상태 업데이트 함수
  async function updateLicenseStatus(license) {
    const { license_id } = license;
    let newStatus = prompt("라이센스 상태를 입력하세요 (예: 허가, 갱신 중, 만료):", license.license_status);
    if (newStatus === null) return; // 취소 시

    const licenseData = {
      license_status: newStatus
    };

    try {
      const response = await axios.patch(`http://localhost:8000/licenses/${license_id}/status`, licenseData, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      console.log("응답:", response.data);
      alert("업데이트 성공!");
      // 업데이트 후 라이센스 목록 갱신
      viewLicense();
    } catch (error) {
      console.error("업데이트 실패:", error.response?.data || error.message);
      if (error.response) {
        errorMessage_upload = `업로드 실패: 허가는 한번에 한 라이센스만 가능합니다.`;
      } else {
        errorMessage_upload = '업로드에 실패했습니다.';
      }
    }
  }

  // PDF 열기 함수
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
    viewLicense();
  });
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
  input, select {
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
  table {
    margin: 20px auto;
    border-collapse: collapse;
    width: 80%;
  }
  th, td {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: left;
  }
  th {
    background: #f4f4f4;
  }
</style>

<div class="page">
  <h2>라이센스 허가</h2>
  <p>관리자 ID: {adminId}</p>

  <h3>라이선스 상태 업데이트</h3>
  {#if errorMessage_upload}
    <p class="error">{errorMessage_upload}</p>
  {/if}
  
  <table>
    <thead>
      <tr>
        <th>License ID</th>
        <th>Pilot ID</th>
        <th>License Number</th>
        <th>License Expiry Date</th>
        <th>License Status</th>
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
          <td>
            <button on:click={() => openPDF(license.license_document)}>PDF 보기</button>
            <button on:click={() => updateLicenseStatus(license)}>상태 업데이트</button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
  
  {#if $loading}
    <p class="loading">로딩 중...</p>
  {/if}

  {#if errorMessage_get}
    <p class="error">{errorMessage_get}</p>
  {/if}

  {#if data_get.length === 0 && !errorMessage_get && !$loading}
    <p>라이센스 정보가 없습니다.</p>
  {/if}
</div>
