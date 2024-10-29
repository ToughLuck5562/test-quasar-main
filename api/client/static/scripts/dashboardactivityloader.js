let currentQuestionIndex = 0;
let score = 0;

async function loadUserActivities() {
    try {
        const response = await fetch(`/get-account-tags?username=${localStorage.getItem('username')}`);
        if (!response.ok) {
            throw new Error('Failed to fetch account tags');
        }

        const tags = await response.json();
        const level = localStorage.getItem('accountlevel');
        const tagsQueryString = tags.map(tag => `tags=${encodeURIComponent(tag)}`).join('&');
        const response2 = await fetch(`/get-activity?level=${level}&${tagsQueryString}`);
        
        console.log(`/get-activity?level=${level}&${tagsQueryString}`);

        if (!response2.ok) {
            throw new Error('Failed to fetch activities');
        }

        const activities = await response2.json();
        createActivityBoxes(activities);
    } catch (error) {
        console.log('Error:', error);
    }
}

function createActivityBoxes(activities) {
    const container = document.querySelector('.container .activities'); 

    activities.forEach(activity => {
        const activityBox = document.createElement('div');
        activityBox.classList.add('activity-box');
        activityBox.innerHTML = `
            <h1 class="activity-box-title">${activity.name}</h1>
            <ul>
                ${activity.tags.map(tag => `<li>#${tag}</li>`).join('')}
            </ul>
            <div>
                <p>${activity.description}</p>
                <button class='start-button'>Start</button>
            </div>
        `;
        
        const button = activityBox.querySelector('.start-button');
        button.addEventListener('click', () => {
            startFlashcards(activity);
        });

        container.appendChild(activityBox);
    });
}

async function startFlashcards(activity) {
    currentQuestionIndex = 0;
    score = 0;

    const existingContainer = document.querySelector('.flashcards-container');
    if (existingContainer) {
        existingContainer.remove();
    }

    const container = document.createElement('div');
    container.className = 'flashcards-container';
    document.body.appendChild(container);

    const flashcardsTags = document.createElement('div');
    flashcardsTags.className = 'flashcards-tags';
    activity.tags.forEach(tag => {
        const tagElement = document.createElement('ul');
        tagElement.innerText = `#${tag}`;
        flashcardsTags.appendChild(tagElement);
    });

    const completionText = document.createElement('p');
    completionText.className = 'flashcard-completion';
    completionText.innerText = `${currentQuestionIndex}/${activity.questions.length}`;

    const questionText = document.createElement('p');
    questionText.innerText = activity.name;

    const flashcardsContent = document.createElement('div');
    flashcardsContent.className = 'flashcards-content';

    const questionElement = document.createElement('h1');
    questionElement.className = 'flashcard-question';
    questionElement.innerText = activity.questions[currentQuestionIndex].Question;

    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'flashcard-options';

    for (const [key, value] of Object.entries(activity.questions[currentQuestionIndex].Answers)) {
        const button = document.createElement('button');
        button.className = `flashcard-option-button ${getButtonClass(key)}`;
        button.innerText = value;

        button.addEventListener('click', () => {
            if (key === activity.questions[currentQuestionIndex].Answer) {
                score++;
            }
            currentQuestionIndex++;
            updateFlashcard(activity);
        });

        optionsContainer.appendChild(button);
    }
    container.appendChild(flashcardsTags);
    container.appendChild(completionText);
    container.appendChild(questionText);
    flashcardsContent.appendChild(questionElement);
    flashcardsContent.appendChild(optionsContainer);
    container.appendChild(flashcardsContent);
}

function getButtonClass(key) {
    switch (key) {
        case 'A': return 'green';
        case 'B': return 'blue';
        case 'C': return 'red';
        case 'D': return 'orange';
        default: return '';
    }
}

function updateFlashcard(activity) {
    if (currentQuestionIndex < activity.questions.length) {
        const completionText = document.querySelector('.flashcard-completion');
        const questionElement = document.querySelector('.flashcard-question');
        const optionsContainer = document.querySelector('.flashcard-options');
        completionText.innerText = `${currentQuestionIndex}/${activity.questions.length}`;
        questionElement.innerText = activity.questions[currentQuestionIndex].Question;
        optionsContainer.innerHTML = '';
        for (const [key, value] of Object.entries(activity.questions[currentQuestionIndex].Answers)) {
            const button = document.createElement('button');
            button.className = `flashcard-option-button ${getButtonClass(key)}`;
            button.innerText = value;

            button.addEventListener('click', () => {
                if (key === activity.questions[currentQuestionIndex].Answer) {
                    score++;
                }
                currentQuestionIndex++;
                updateFlashcard(activity);
            });

            optionsContainer.appendChild(button);
        }
    } else {
        endFlashcards();
    }
}

function endFlashcards() {
    const container = document.querySelector('.flashcards-container');
    if (!container) return;
    container.innerHTML = '';

    const summaryText = document.createElement('p');
    summaryText.innerText = `You scored ${score} out of ${currentQuestionIndex}.`;
    
    const leaveButton = document.createElement('button');
    leaveButton.innerText = 'Leave';
    leaveButton.classList.add('d13m1')
    leaveButton.addEventListener('click', () => {
        container.remove();
    });

    container.appendChild(summaryText);
    container.appendChild(leaveButton);
}
loadUserActivities();
