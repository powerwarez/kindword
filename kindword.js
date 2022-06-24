const HF_API_TOKEN = "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";
const model = "kindword-klue_bert-base";

const data = { inputs: "안녕하세요" };

const response = await fetch(
  `https://api-inference.huggingface.co/models/${model}`,
  {
    headers: { Authorization: `Bearer ${HF_API_TOKEN}` },
    method: "POST",
    data: JSON.stringify(data),
  }
);
const dataResponse = await response.json();
console.log(dataResponse);
