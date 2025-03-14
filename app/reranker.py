from transformers import AutoTokenizer, AutoModel
from langchain.schema import Document
import torch.nn.functional as F
import torch

class CustomColBERTCompressor:
    """
    ColBERT 방식의 Late Interactio Score를 사용하여 문서를 필터링하고 압축하는 Custom Compressor
    """

    def __init__(self, model_name, threshold: float = 0.3, top_k: int = 5):
        """
        Args:
            tokenizer: ColBERT 방식의 토크나이저(Hugging Face Tokenizer)
            model: ColBERT 방식의 임베딩 모델(Hugging Face Model)
            threshold (float): 유사도 점수의 최소 임계값 (이 값보다 낮으면 필터링링)
            top_k (int): 가장 관련성이 높은 상위 k개 문서만 유지
        """

        self.model = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.threshold = threshold
        self.top_k = top_k

    def compress_documents(self, documents: list[Document], query: str) -> list[Document]:
        """
        ColBERT 기반 Late Interaction Score를 사용하여 문서의 중요도를 평가하고 압축.
        """
        if not documents:
            return []

        query_embeddings = encode_query(query, self.tokenizer, self.model)
        scored_docs = []

        for doc in documents:
            doc_embeddings = encode_document(doc, self.tokenizer, self.model)
            score = late_interaction_score(query_embeddings, doc_embeddings)

            if score > self.threshold:
                scored_docs.append((doc, score))

        sorted_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)[
            :self.top_k]

        return [doc for doc, _ in sorted_docs]


def encode_document(doc: Document, tokenizer, model):
    """LangChain Document 객체를 ColBERT 방식으로 벡터화"""
    text = doc.page_content
    inputs = tokenizer(text, return_tensors="pt",
                       padding=True, truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model(**inputs)

    token_embeddings = outputs.last_hidden_state

    return token_embeddings.squeeze(0)


def encode_query(text, tokenizer, model):
    """텍스트를 ColBERT 방식으로 벡터화"""
    inputs = tokenizer(text, return_tensors="pt",
                       padding=True, truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model(**inputs)

    # 토큰별 벡터를 추출
    token_embeddings = outputs.last_hidden_state

    return token_embeddings.squeeze(0)


def late_interaction_score(query_embeddings, doc_embeddings):
    """ColBERT Late Interactio Score 계산"""

    # 질의 토큰과 문서 토큰 간 코사인 유사도 계산
    similarity_matrix = F.cosine_similarity(
        query_embeddings.unsqueeze(1),
        doc_embeddings.unsqueeze(0),
        dim=-1
    )

    # 각 질의 토큰별로 가장 유사한 문서 토큰 선택 후 평균 점수 반환
    max_sim_per_query_token = torch.max(similarity_matrix, dim=1).values
    score = torch.mean(max_sim_per_query_token)

    return score.item()

if __name__ == "__main__":
    # Test
    model_name = "bert-base-uncased"
    compressor = CustomColBERTCompressor(model_name, threshold=0.4, top_k=5)

    query = "What is the capital of France?"
    documents = [
        Document(page_content="Paris is the capital of France."),
        Document(page_content="The Eiffel Tower is located in Paris."),
        Document(page_content="France is a country in Europe.")
    ]

    compressed_docs = compressor.compress_documents(documents, query)
    for doc in compressed_docs:
        print(doc.page_content)
