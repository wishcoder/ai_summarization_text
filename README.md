# Large Text Summarization Using LLM
Summarization large text using Vertex AI Language Models 'text-bison@001'

## Publicly available corpus of emails
* https://www.cs.cmu.edu/~./enron/

## Text Summarization Methods using Vertex AI PaLM API
* https://codelabs.developers.google.com/text-summ-large-docs-stuffing#0
* [Code](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/use-cases/document-summarization/summarization_large_documents.ipynb)

## Google Foundational Models
Google's current policy restricts downloading foundational models like Gemini for on-premise deployment. These models are highly complex and require significant computational resources to run effectively.  However, there are alternative solutions you can explore within GCP that adhere to your company's security policies:

### [Vertex AI](https://cloud.google.com/vertex-ai/docs) Private Endpoints
> [!TIP]
> Vertex AI offers the option to deploy models within a Virtual Private Cloud (VPC) environment. This allows you to access the model without any data leaving your network. You can configure a Private Endpoint for your Gemini model within your VPC. Refer to the [Vertex AI documentation on Private Endpoints](https://cloud.google.com/vertex-ai/docs/predictions/using-private-endpoints) for details on setup.

### Custom TensorFlow Model Training 
> [!TIP]
> While downloading pre-trained models isn't feasible, you could consider training a custom model based on Google's open-source TensorFlow libraries. This approach would require expertise in TensorFlow and potentially significant training time depending on the amount of data you have. However, the resulting model would reside entirely within your GCP project and wouldn't require sending data externally.
 
### Pros and cons of each approach
> [!TIP]
>
>| Approach                         | Pros                                           | Cons                                                                                   |
>|----------------------------------|------------------------------------------------|----------------------------------------------------------------------------------------|
>| **Vertex AI Private Endpoints**    | - Keeps data within your VPC<br>- Leverages pre-trained Gemini model's capabilities | - Requires additional configuration for VPC and Private Endpoints                      |
>| **Custom TensorFlow Model Training** | - Full control over model and data             | - Requires significant expertise and training time<br>- May not achieve the same level of performance as pre-trained Gemini |


## Google's policy regarding customer data usage for LLM pre-training 

### Vertex AI Products
> [!TIP]
> According to Google Cloud's documentation, they do not use customer data to train or fine-tune foundational models like Gemini (used in Vertex AI) without the customer's prior permission or instruction. This means your data used within Vertex AI services stays within your project or VPC environment for AI tasks.

### Vertex AI Customer Data Processing Addendum (CDPA)
> [!TIP]
> [Vertex AI Customer Data Processing Addendum (CDPA)](https://cloud.google.com/terms/data-processing-addendum) (details how Google processes customer data)
 
### Solved: Re: Privacy of Data on LLM - Google Cloud Community
> [!TIP]
> [Google Cloud Community](https://www.googlecloudcommunity.com/gc/AI-ML/Privacy-of-Data-on-LLM/m-p/645360) (discusses customer data usage for Vertex AI models)
 
