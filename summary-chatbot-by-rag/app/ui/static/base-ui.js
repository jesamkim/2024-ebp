function getYouHtml(question) {
  return `<div class="event custom-event-you">
    <div class="content">
      <div class="summary">
        <a>YOU</a>
      </div>
      <div class="extra text custom-extra-text custom-chat-text">
        ${question}
      </div>
      <div class="meta">
      </div>
    </div>
  </div>
  `
}

function getAiHtml(answer, reference_documents, documentIndex) {
  // let reference_texts = '<div class = "ui bulleted list" >'
  let reference_texts = ''
  for (let idx in reference_documents) {
    console.log(reference_documents[idx])
    reference_texts += `
      <div><h3>👏FOUND👏</H3></div>
      <div>---------------------</div>
      <div><strong>Sentence</strong></div>
      <div class = "ui bulleted list" >
        <div class="item" >${reference_documents[idx]['content']} </div>
      </div>
      <div><strong>Question</strong></div>
      <div class = "ui bulleted list" >
        <div class="item" >${reference_documents[idx]['metadata']['question']} </div>
      </div>
      
      <div><strong>Answer</strong></div>
      <div class = "ui bulleted list" >
        <div class="item" >${reference_documents[idx]['metadata']['answer']} </div>
      </div>
    `

    // <div class="item" >question: ${reference_documents[idx]['metadata']['question']} </div>
    // <div class="item" >answer: ${reference_documents[idx]['metadata']['answer']} </div>
  }
  // reference_texts += '</div>'

  return `
  <hr class="dotted">
  <div class="event custom-event-ai">
  </div>
    <div class="content">
      <div class="summary">
<!--        <a>AI</a> <span style="color: #000000;"></span>-->
      </div>
<!--      <div class="extra text custom-extra-text custom-chat-text">-->
        <pre>
${answer}
        </pre>
<!--      </div>-->
      <div class="meta">
      </div>
    </div>
  </div>
  
  <div class="ui fluid accordion">
    <div class="title">
      <i class="dropdown icon"></i>
      ${documentIndex}
    </div>
    <div class="content">
      ${reference_texts}
    </div>
  </div>
  `
}

function getDocuments(callback) {
  $.ajax({
    url: "/documents",
    type: "GET",
    success: function (result) {
      callback(result)
    },
    error: function (error) {
      console.log(error)
    }
  })
}

function deleteDocuments(documentIndex, success, fail) {
  $.ajax({
    url: `/documents/${documentIndex}`,
    type: "DELETE",
    success: function (result) {
      success(result)
    },
    error: function (error) {
      fail(error)
    }
  })
}

function uploadDocument(file, documentIndex, success, fail) {
  const data = new FormData();
  data.append('file', file);
  $.ajax({
    url: `/documents/${documentIndex}`,
    type: "POST",
    data: data,
    headers: {
      'Accept': 'application/json',
    },
    crossDomain: true,
    contentType: false,
    processData: false,
    dataType: 'json',
    cache: false,
    success: function (result) {
      success(result)
    },
    error: function (error) {
      fail(error)
    }
  })
}

function getAnswer(question, modelId, maxTokens, temperature, topP, topK, callback) {
  // Get Prompt
  let prompt = document.getElementById('custom-prompt-textarea').innerText

  $.ajax({
    url: `/answer/${question}`,
    type: "POST",
    data: JSON.stringify({
      'modelId': modelId,
      'maxTokens': maxTokens,
      'temperature': temperature,
      'topP': topP,
      'topK': topK,
      'prompt': prompt
    }),
    dataType: 'json',
    contentType: "application/json; charset=utf-8",
    success: function (result) {
      callback(result)
    },
    error: function (error) {
      console.log(error)
      inactiveProgress()
    }
  })
}

function getAnswerWithRetrieval(indexName, question, modelId, maxTokens, temperature, topP, topK, callback) {
  // Dummy
  question = "dummy"

  // Get Prompt
  let prompt = document.getElementById('custom-prompt-textarea').innerText

  $.ajax({
    url: `/answer/${indexName}/${question}`,
    type: "POST",
    data: JSON.stringify({
      'modelId': modelId,
      'maxTokens': maxTokens,
      'temperature': temperature,
      'topP': topP,
      'topK': topK,
      'prompt': prompt
    }),
    dataType: 'json',
    contentType: "application/json; charset=utf-8",
    success: function (result) {
      callback(result)
    },
    error: function (error) {
      console.log(error)
      inactiveProgress()
    }
  })
}

function activeProgress() {
  $('#custom-progress-icon').addClass('active')
}

function inactiveProgress() {
  $('#custom-progress-icon').removeClass('active')
}

function initializeAccordion() {
  $('.ui.accordion')
    .accordion()
  ;
}

window.addEventListener('DOMContentLoaded', function () {
  // Set input enter event
  let sendButton = document.getElementById('custom-send-button')
  let questionInput = document.getElementById('custom-question-input')

//   questionInput.value=`
// 아래 <contents></contents> 태그 안에서 <instruction></instruction>의 내용만 요약해주세요.
// 구체적인 수치를 제시하고 한글로 작성해주세요. 오직 보고서 내용으로만 요약해야 하며, 인터넷 검색이나 보고서에서 언급하지 않은 다른 서적의 내용은 참고하지 말아주세요.
//
// <contents>
// {contents}
// </contents>
//
// <instruction>
// 1. 연구의 배경 및 대상
// 1.1 연구의 배경 및 목적
// 1.2 연구 대상 및 방법
//
// 2. 연구내용 및 주요 분석 결과
// 2.1 국제 재생에너지 시장동향 분석
// 2.2 국제 재생에너지 정책동향 분석
// 2.3 국가별 재생에너지 제도의 보급효과 실증분석
//
// 3. 결론
// 3.1 정책적 시사점
// 3.2 연구의 한계 및 향후 과제
// </instruction>
//
// 서두는 작성하지 말아줘.
//  `


  questionInput.addEventListener("keypress", function (event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      sendButton.click();
    }
  });

  // Set input send event
  sendButton.addEventListener('click', function () {
    // Get chat ui
    let feeds = document.getElementById('custom-feeds')

    // Update question to View
    let question = document.getElementById('custom-question-input').value

    // feeds.insertAdjacentHTML('beforeend', getYouHtml(question))
    feeds.scrollIntoView(false);

    // Remove special character
    // let reg = /[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gim;
    let reg = /[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gim;
    question = question.replace(reg, '')

    // Get Document
    let dropdownMenu = document.getElementById('custom-indices-dropdown-menu')
    let selects = dropdownMenu.getElementsByClassName("selected");

    // Get Model Parameters
    let modelId = 'anthropic.claude-v2'
    let maxTokens = document.getElementById('custom-max-tokens-input').value
    let temperature = document.getElementById('custom-temperature-input').value
    let topP = document.getElementById('custom-top-p-input').value
    let topK = document.getElementById('custom-top-k-input').value


    if (selects.length > 0) {

      // Update answer to View
      activeProgress()

      let indexName = selects[0].getAttribute('data-value')
      console.log(`${indexName} is selected - Call LLM model with Retrieval`)

      getAnswerWithRetrieval(indexName, question, modelId, maxTokens, temperature, topP, topK, function (result) {
        console.log(result)
        let answer = result['result']
        let referenceDocuments = result['reference_documents']
        feeds.insertAdjacentHTML('beforeend', getAiHtml(answer, referenceDocuments, indexName))
        feeds.scrollIntoView(false);
        initializeAccordion()
        inactiveProgress()
      })
    } else {
      // console.log('Document not selected - Call Only LLM model')
      // getAnswer(question, modelId, maxTokens, temperature, topP, topK, function (result) {
      //   console.log(result)
      //   let answer = result['result']
      //   feeds.insertAdjacentHTML('beforeend', getAiHtml(answer, [], '-'))
      //   feeds.scrollIntoView(false)
      //   initializeAccordion()
      //   inactiveProgress()
      // })
    }

    // Clean
    document.getElementById('custom-question-input').value = ""
  })


  // Set dropdown and document list event
  let dropDownMenu = document.getElementById('custom-indices-dropdown-menu')
  let deleteDocumentList = document.getElementById('custom-documents-deletion')

  function loadDocuments(callback) {
    getDocuments(function (result) {
      dropDownMenu.innerHTML = ''
      deleteDocumentList.innerHTML = ''
      // dropDownMenu.dropdown('set selected', result[0]);
      for (let idx in result) {
        // Set to Documents for retrieval
        let menuHtml = `<div class="item" data-value="${result[idx]}">${result[idx]}</div>`
        dropDownMenu.insertAdjacentHTML('beforeend', menuHtml)

        // Set to Documents for delete
        let deleteHtml = `
          <a class="item">
            ${result[idx]}
            <div class="ui orange horizontal label custom-del-items" data-value="${result[idx]}">DEL</div>
          </a>
          `
        let conditions = ['doc-ant-grasshoper', 'doc-little-red-hood', 'doc-tortoise-hare']
        if (conditions.some(el => result[idx].includes(el))) {
          deleteHtml = `
          <a class="item">
            ${result[idx]}
            <div class="ui green horizontal label" data-value="${result[idx]}">Fixed</div>
          </a>
          `
        }

        deleteDocumentList.insertAdjacentHTML('beforeend', deleteHtml)
      }

      $('#custom-documents-selection')
        .dropdown({
          clearable: true
        }).dropdown('set selected', result[0])
      if (callback) {
        callback(result)
      }
    })
  }

  activeProgress()
  loadDocuments(function (result) {
    inactiveProgress()
  })

  // Set document delete event
  $(document).on('click', ".custom-del-items", function (event) {
    event.stopPropagation();
    event.stopImmediatePropagation();

    let sendButton = $(event.target);
    let documentIndex = sendButton.attr('data-value')
    console.log(documentIndex)

    activeProgress()
    deleteDocuments(documentIndex, function (result) {
      console.log(result)
      loadDocuments(function (result) {
        inactiveProgress()
      })
    }, function (error) {
      console.log(error)
      inactiveProgress()
    })
  });

  // Set file input event
  $(document).on('change', '#custom-file-input', function (event) {
    if (this.files.item.length > 0) {
      let filename = this.files.item(0).name
      $('#custom-doc-name-input').val(filename.toLowerCase())
    }
  })


  function cleanForm() {
    document.getElementById("custom-file-input").value = "";
    $('#custom-doc-name-input').val('')
    $('#custom-doc-chunk-input').val(1000)
    $('#custom-doc-overlap-input').val(0)
  }

  // Set file upload event
  $(document).on('click', "#custom-doc-upload", function (event) {
    event.stopPropagation();
    event.stopImmediatePropagation();
    let documentFileInput = document.getElementById("custom-file-input");
    let documentFile = documentFileInput.files[0]
    let documentIndex = $('#custom-doc-name-input').val()

    activeProgress()
    uploadDocument(documentFile, documentIndex, function (result) {
      console.log(result)
      loadDocuments(function (result) {
        cleanForm()
        inactiveProgress()
      })
    }, function (error) {
      console.log(error)
      inactiveProgress()
      cleanForm()
    })

  });

  $('#openModal').click(function () {
    $('#inputModal').modal('show');
  });

  $('#closeModal').click(function () {
    $('#inputModal').modal('hide');
  });

  $('#inputModal').modal({
    closable: true,
    onHide: function () {
      console.log('hidden');
      let promptText = document.getElementById('custom-prompt-textarea')
      promptText.innerText = promptText.value
    },
  });


})

