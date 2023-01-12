const {useState} = React;

const init_prompt = "I want you to write program in Python. You are allowed to respond only in JSON. No explanation. No English text.\n"+
"Program: Program generates and prints output\n"+
"Program Input: No input\n"+
"Program Output: Hello World\n"+
"Respond with JSON having one field \"CODE\" with Python code.";

let prompt = init_prompt;

function CodeView()
{
    const [displayedText, setDisplayedText] = useState("");
    // // TO DO: make fetch request to local server
    setInterval(function() {
        fetch(`${window.location.origin}/read/dummy.py`)
        .then(response => response.text())
        .then(text     => setDisplayedText(text))
        .catch(error   => console.error('Error:', error));
    }, 1000);

    return (
        <div>
            <h2>Generated Code:</h2>
            <p style={{whiteSpace: 'pre'}}>{displayedText}</p>
        </div>
    );
};

function PromptInput()
{
    const [message, setMessage] = useState(init_prompt);

    const handleMessageChange = event => {
        // 👇️ access textarea value
        setMessage(event.target.value);
        prompt = event.target.value;
    };

    const onPressGenerate = event => {
        fetch(`${window.location.origin}/buttons/start`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                  },
                body: JSON.stringify({
                    "prompt":prompt,
                    "API": document.getElementById("dAPI").textContent
                })
            }
        ).catch(error   => console.error('Error:', error));
    }

    const onPressStop = event => {
        fetch(`${window.location.origin}/buttons/stop`,
            {
                method: 'POST'
            }
        ).catch(error   => console.error('Error:', error));
    }

    const onDropdownChoice = event =>
    {
        document.getElementById("dAPI").textContent = event.target.text;
    }

    return (
        <div>
            <textarea  style={{width: "100%",height: "150px"}}
                type="text" id="fname" name="fname" value={message} onChange={handleMessageChange}>
            </textarea>
            <button onClick={onPressGenerate} className="btn btn-primary m-1" title="Send Prompt">Generate</button>
            <button onClick={onPressStop} className="btn btn-primary m-1" title="Send Prompt">Stop</button>

            <div className="btn-group">
                <button type="button" id="dAPI" className="btn btn-primary m-1 dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    revChatGPT
                </button>
                <div className="dropdown-menu" aria-labelledby="dLabel">
                    <a className="dropdown-item" onClick={onDropdownChoice} href="#">revChatGPT</a>
                    <a className="dropdown-item" onClick={onDropdownChoice} href="#">OpenAIAPI</a>
                </div>
            </div>
        </div>
    );
};

function PromptResponse()
{
    const [displayedResponse, setDisplayedResponse] = useState("");
    // // TO DO: make fetch request to local server
    setInterval(function() {
        fetch(`${window.location.origin}/GPTresponse`)
        .then(response => response.text())
        .then(text     => setDisplayedResponse(text))
        .catch(error   => console.error('Error:', error));
    }, 1000);

    return (
        <div>
          <p style={{whiteSpace: 'pre'}}>{displayedResponse}</p>
        </div>
    );
};


ReactDOM.render(
    <div className="container">
        <div className="row">
            <div className="col-sm">
                <CodeView></CodeView>
            </div>
            <div className="col-sm">
                <PromptInput></PromptInput>
                <PromptResponse></PromptResponse>
            </div>
        </div>
    </div>
    ,document.getElementById('root')
);