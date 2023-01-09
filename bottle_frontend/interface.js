const {useState} = React;
console.log(React)

const init_prompt = "I want you to write program in Python. You are allowed to respond only in JSON. No explanation. No English text.\n"+
"Program: Program generates and prints output\n"+
"Program Input: No input\n"+
"Program Output: Hello World\n"+
"Respond with JSON having one field \"CODE\" with Python code.";

let prompt = init_prompt;

function CodeView()
{
    const [displayedText, setDisplayedText] = useState("");
    // TO DO: make fetch request to local server
    fetch(`${window.location.origin}/read/dummy.py`)
    .then(response => response.text())
    .then(text     => setDisplayedText(text))
    .catch(error   => console.error('Error:', error));

    return (
        <div>
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

    const onPressSend = event => {
        fetch(`${window.location.origin}/buttons/start`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                  },
                body: JSON.stringify({
                    "prompt":prompt,
                    "test":"test"
                })
            }
        ).catch(error   => console.error('Error:', error));
    }

    return (
        <div>
            <textarea  style={{width: "100%",height: "150px"}}
                type="text" id="fname" name="fname" value={message} onChange={handleMessageChange}>
            </textarea>
            <button onClick={onPressSend} className="btn btn-primary" title="Send Prompt" color="#841584">Generate</button>
        </div>
    );
};

function PromptResponse()
{
    return (
        <div>
          <p>Hello</p>
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