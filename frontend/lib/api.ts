import axios from "axios";

// Configure axios instance for reuse
const apiClient = axios.create({
  baseURL: "https://127.0.0.1:8000", // NOTE: https
  timeout: 30000,
  headers: {
    Accept: "application/json",
  },
  withCredentials: true, // This can go here instead of an interceptor
});


// Add CORS support for the client
apiClient.interceptors.request.use(config => {
  config.withCredentials = true;
  return config;
});

export async function analyzeFile(
  audioFile: File,
  options?: {
    referenceNotes?: string;
    sheetMusic?: File;
  }
) {
  const formData = new FormData();
  formData.append("audio_file", audioFile);
  
  if (options?.referenceNotes) {
    formData.append("reference", options.referenceNotes);
  }
  
  if (options?.sheetMusic) {
    formData.append("sheet_music", options.sheetMusic);
  }

  try {
    const response = await apiClient.post("/analyze", formData, {
      // For tracking upload progress:
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / (progressEvent.total || 1)
        );
        console.log(`Upload progress: ${percentCompleted}%`);
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const errorData = error.response?.data;
      console.error("API Error:", {
        status: error.response?.status,
        data: errorData,
        config: error.config,
      });
      
      throw new Error(
        errorData?.detail || 
        errorData?.message || 
        `Analysis failed (${error.response?.status || "no status"}). Please try again.`
      );
    }
    throw error;
  }
}