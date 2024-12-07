<script>
  import { userId } from '../../../stores.js';
  import axios from 'axios';
  import { writable } from 'svelte/store';
  import { onMount } from 'svelte';

  $: pilotId = $userId;

  let license_number = '';
  let license_expiry_date = '2020-01-01';
  let file; // PDF 파일

  let data_get = []; // 배열로 변경
  const loading = writable(false);
  let errorMessage_get = '';

  async function viewLicense() {
    loading.set(true);
    let endpoint_get = 'http://localhost:8000/licenses'; // 다수 라이센스 반환 API 엔드포인트 (예: 배열 반환)

    try {
      const response = await axios.get(endpoint_get, { params: { pilot_id: pilotId } });

      if (Array.isArray(response.data)) {
        // 배열 형태로 반환받는다고 가정
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
      alert("파일을 선택하세요!");
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
  table {
    margin: 20px auto;
    border-collapse: collapse;
    width: 80%;
  }
  th, td {
    border: 1px solid #ccc;
    padding: 10px;
    text-align:left;
  }
  th {
    background: #f4f4f4;
  }
</style>

<div class="page">
  <h2>라이센스 업데이트</h2>
  <p>파일럿 ID: {pilotId}</p>

  <h3>라이선스 업로드</h3>
  <form on:submit|preventDefault={uploadLicense}>
    <label>
      라이선스 번호:
      <input type="text" bind:value={license_number} />
    </label>
    <br />
    <label>
      라이선스 만료일:
      <input type="date" bind:value={license_expiry_date} />
    </label>
    <br />
    <label>
      PDF 파일 업로드:
      <input type="file" accept="application/pdf" on:change={handleFileChange} />
    </label>
    <br />
    <button type="submit">업로드</button>
  </form>

  <h3>파일럿 라이센스 정보</h3>
  {#if $loading}
    <p class="loading">로딩 중...</p>
  {/if}

  {#if errorMessage_get}
    <p class="error">{errorMessage_get}</p>
  {/if}

  {#if data_get && data_get.length > 0 && !errorMessage_get}
    <table>
      <thead>
        <tr>
          <th>license_id</th>
          <th>pilot_id</th>
          <th>license_number</th>
          <th>license_expiry_date</th>
          <th>license_status</th>
          <!-- <th>license_document(Base64)</th> -->
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
            <!-- <td style="max-width:200px; word-break:break-all;">{license.license_document}</td> -->
            <td><button on:click={() => openPDF(license.license_document)}>PDF 보기</button></td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>
