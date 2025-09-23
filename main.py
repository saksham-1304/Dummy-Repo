import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db
import time
import os

# Page configuration
st.set_page_config(
    page_title="Codebasics Q&A Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Card styling */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    /* Status indicators */
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .status-info {
        background: #d1ecf1;
        color: #0c5460;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    
    .status-warning {
        background: #fff3cd;
        color: #856404;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    
    /* Answer styling */
    .answer-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .answer-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .answer-text {
        font-size: 1rem;
        line-height: 1.6;
        color: #34495e;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Metrics styling */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e1e5e9;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        margin-top: 0.25rem;
    }
    
    /* Loading animation */
    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin-right: 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'knowledge_base_created' not in st.session_state:
    st.session_state.knowledge_base_created = os.path.exists("faiss_index")
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Main header
st.markdown("""
<div class="main-header">
    <h1>🎓 Codebasics Q&A Assistant</h1>
    <p>Get instant answers to your learning questions powered by AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🛠️ Control Panel")
    
    # Knowledge base status
    if st.session_state.knowledge_base_created:
        st.markdown("""
        <div class="status-success">
            ✅ Knowledge Base Ready
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-warning">
            ⚠️ Knowledge Base Not Created
        </div>
        """, unsafe_allow_html=True)
    
    # Create knowledge base button
    if st.button("🔄 Create/Update Knowledge Base", use_container_width=True):
        with st.spinner("Building knowledge base..."):
            try:
                create_vector_db()
                st.session_state.knowledge_base_created = True
                st.success("✅ Knowledge base created successfully!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error creating knowledge base: {str(e)}")
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📊 Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Questions Asked</div>
        </div>
        """.format(len(st.session_state.chat_history)), unsafe_allow_html=True)
    
    with col2:
        kb_status = "Active" if st.session_state.knowledge_base_created else "Inactive"
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">KB Status</div>
        </div>
        """.format(kb_status), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sample questions
    st.markdown("### 💡 Sample Questions")
    sample_questions = [
        "Do you provide job assistance?",
        "Do you have JavaScript course?",
        "Should I learn Power BI or Tableau?",
        "Can I use Power BI on Mac?",
        "Do you offer EMI payments?",
        "What are the prerequisites?"
    ]
    
    for i, question in enumerate(sample_questions):
        if st.button(f"📝 {question}", key=f"sample_{i}", use_container_width=True):
            st.session_state.current_question = question

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Question input
    st.markdown("### 🤔 Ask Your Question")
    
    # Use session state for question if set from sample questions
    default_question = st.session_state.get('current_question', '')
    question = st.text_input(
        "Type your question here...",
        value=default_question,
        placeholder="e.g., Do you provide job assistance?",
        help="Ask any question about Codebasics courses, pricing, or policies"
    )
    
    # Clear the session state question after using it
    if 'current_question' in st.session_state:
        del st.session_state.current_question
    
    # Process question
    if question and st.session_state.knowledge_base_created:
        with st.spinner("🔍 Searching for the best answer..."):
            try:
                chain = get_qa_chain()
                response = chain(question)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'question': question,
                    'answer': response["result"],
                    'timestamp': time.strftime("%H:%M:%S")
                })
                
                # Display answer
                st.markdown("### 💬 Answer")
                st.markdown(f"""
                <div class="answer-container">
                    <div class="answer-header">
                        🤖 AI Assistant Response
                    </div>
                    <div class="answer-text">
                        {response["result"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show source confidence
                if response.get("source_documents"):
                    with st.expander("📚 View Source Information"):
                        st.write(f"**Found {len(response['source_documents'])} relevant sources:**")
                        for i, doc in enumerate(response["source_documents"][:3]):
                            st.write(f"**Source {i+1}:** {doc.metadata.get('source', 'Unknown')}")
                            st.write(f"*Content preview:* {doc.page_content[:200]}...")
                            st.write("---")
                
            except Exception as e:
                st.error(f"❌ Error processing question: {str(e)}")
    
    elif question and not st.session_state.knowledge_base_created:
        st.markdown("""
        <div class="status-warning">
            ⚠️ Please create the knowledge base first using the button in the sidebar.
        </div>
        """, unsafe_allow_html=True)

with col2:
    # Features panel
    st.markdown("### ✨ Features")
    
    features = [
        {
            "icon": "🤖",
            "title": "AI-Powered",
            "description": "Uses Google Gemini LLM for accurate responses"
        },
        {
            "icon": "⚡",
            "title": "Instant Answers",
            "description": "Get responses in seconds, not hours"
        },
        {
            "icon": "📚",
            "title": "Comprehensive KB",
            "description": "Trained on real Codebasics FAQs"
        },
        {
            "icon": "🎯",
            "title": "Context-Aware",
            "description": "Understands your specific questions"
        }
    ]
    
    for feature in features:
        st.markdown(f"""
        <div class="feature-card">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{feature['icon']}</div>
            <div style="font-weight: 600; margin-bottom: 0.25rem;">{feature['title']}</div>
            <div style="font-size: 0.9rem; color: #666;">{feature['description']}</div>
        </div>
        """, unsafe_allow_html=True)

# Chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 📝 Recent Questions")
    
    # Show last 5 questions
    for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
        with st.expander(f"🕐 {chat['timestamp']} - {chat['question'][:50]}..."):
            st.write(f"**Q:** {chat['question']}")
            st.write(f"**A:** {chat['answer']}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🎓 Powered by Codebasics | Built with Streamlit & LangChain</p>
    <p style="font-size: 0.8rem;">This AI assistant is trained on Codebasics course information and FAQs</p>
</div>
""", unsafe_allow_html=True)