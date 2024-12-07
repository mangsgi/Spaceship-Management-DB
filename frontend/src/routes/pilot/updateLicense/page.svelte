<script>
  // FindPilotFlight 페이지에 필요한 로직 추가
  import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정

  $: pilotId = $userId;

  let license_number = 0;
  let license_expiry_date = '2020-01-01';
  let file; // PDF 파일

  let data_get= {};

  async function viewLicense() {

  loading.set(true);

  let endpoint_get = 'http://localhost:8000/licenses';

  try {
    const response = await axios.get(endpoint_get, { params: { pilot_id: pilotId } });

    // 임시 조건 (실제 응답 검증으로 대체)
    if (response.data && response.data.pilot_id === pilotId) {
      // 역할에 따른 URL로 네비게이션
      data_get = response.data;
      
    } 
  } catch (error) {
    console.error('데이터를 가져오는 중 오류 발생:', error);
    if (error.response) {
      // 서버 응답 오류 처리
      if (error.response.status === 400) {
        errorMessage_get = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
      } else {
        errorMessage_get = `서버 오류 발생: ${error.response.status}`;
      }
    } else {
      // 요청이 서버에 도달하지 못한 경우
      errorMessage_get = '서버에 연결할 수 없습니다.';
    }
  } finally {
    loading.set(false);
  }
  }

  async function uploadLicense() {
      const formData = new FormData();

      // JSON 데이터를 Blob으로 추가
      const licenseData = {
          license_number,
          license_expiry_date,
      };
      formData.append("license_data", new Blob([JSON.stringify(licenseData)], { type: "application/json" }));

      // 파일 추가
      if (file) {
          formData.append("license_file", file);
      } else {
          alert("파일을 선택하세요!");
          return;
      }

      try {
          const response = await axios.post("/pilots/1/licenses", formData, {
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
      file = event.target.files[0]; // 선택한 파일을 변수에 저장
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
    <h2>라이센스 업데이트</h2>
    <p>파일럿 ID: {pilotId}</p>
    <!-- 하위 페이지 내용 추가 -->
     <!-- UI -->
    <h3>라이선스 업로드</h3>
    <form on:submit|preventDefault={uploadLicense}>
        <label>
            라이선스 번호:
            <input type="number" bind:value={license_number} />
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

    <h3>파일럿 라이센스 info</h3>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Contact Info</th>
          <th>Emergency Contact</th>
        </tr>
      </thead>
      <tbody>
          <tr>
            <td>{data_get.license_id}</td>
            <td>{data_get.contact_info}</td>
            <td>{data_get.emergency_contact}</td>
          </tr>
      </tbody>
    </table>
  </div>


