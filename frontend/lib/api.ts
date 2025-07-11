import axios from "axios";

export async function analyzeFile(
  audioFile: File,
  options?: {
    referenceNotes?: string;
    sheetMusic?: File;
  }
) {
  const formData = new FormData();
  
  // Use 'audio_file' to match FastAPI's expected parameter name
  formData.append("audio_file", audioFile);
  
  if (options?.referenceNotes) {
    formData.append("reference", options.referenceNotes);
  }
  
  if (options?.sheetMusic) {
    formData.append("sheet_music", options.sheetMusic);
  }

  try {
    const response = await axios.post("http://localhost:8000/analyze", formData, {
      // Let axios set the content-type automatically
      headers: {
        "Accept": "application/json",
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const errorData = error.response?.data;
      console.error("API Error Details:", {
        status: error.response?.status,
        data: errorData,
        headers: error.response?.headers,
      });
      
      throw new Error(
        errorData?.detail || 
        errorData?.message || 
        "Analysis failed. Please check your input and try again."
      );
    }
    throw error;
  }
}