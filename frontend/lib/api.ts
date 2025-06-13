import axios from "axios";

export async function analyzeFile(file: File, referenceNotes?: string) {
  const formData = new FormData();
  formData.append("file", file);
  if (referenceNotes) formData.append("reference", referenceNotes);

  const response = await axios.post("http://localhost:8000/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}
