var q_no = 1;

$(function() {
	Main();
});


function Main() {
	$("#input-startdate , #input-enddate").datetimepicker();
	Map();
	$("#add-question-button").click(function() {
		AddQuestion();
		q_no += 1;
		return false;
	}).trigger('click');
	EventHandler();
}

var question_area = "";
var ans_no = new Array();
function AddQuestion() {
	question_area  = '<div class="form-group">\
					    <label for="exampleInputEmail1">Question No.' + q_no + '</label>\
					    <textarea class="form-control inputQuestion" topic="' + q_no + '"></textarea>\
					  </div>\
					  <div class="form-group">\
					    <label for="exampleInputPassword1">Answer <button type="submit" class="btn btn-default add-answer-button" topic="' + q_no + '">+</button></label>\
					      <div class="checkbox answer-section" topic="' + q_no + '">\
					      </div>\
					  </div><hr>';
	$("#question-section").append(question_area);
	$(".inputQuestion[topic='" + q_no + "']").wysihtml5();

	ans_no[q_no] = 1;
	$(".add-answer-button[topic='" + q_no + "']").click(function() {
		var question_no = $(this).attr('topic');
		AddAnswer(question_no,ans_no[question_no]);
		ans_no[question_no]++;
		return false;
	}).trigger('click');
}

var answer_area =  "";
function AddAnswer(question_no,answer_no) {
	answer_area = '<div class="input_answer">\
					<input type="checkbox"> <input style="margin-bottom:5px;" type="text" class="form-control" placeHolder="Answer No.' + answer_no + '">\
					</div>';
	$(".answer-section[topic='" + question_no + "']").append(answer_area);

}

function Map() {
	$("#point-location").gmap3();
}

var event_data = {};
var question_data = [];
function EventHandler() {
	$("#save-event-button").click(function() {
		// SendQuestionData();
		SendEventData();
		return false;
	});

	$("#modify-event-button").click(function() {
		// SendQuestionData();
		SendModifyEventData();
		return false;
	});

	$("#save-question-button").click(function() {
		SendQuestionData();
		// SendEventData();
		return false;
	});
}

function SendEventData() {
	var title = $("#input-title").val();
	var description = $("#input-description").val();
	var startdate = $("#input-startdate").val();
	var enddate = $("#input-enddate").val();
	var location = $("#input-location").val();
	event_data = {
		title : title,
		description : description, 
		startdate : startdate,
		enddate : enddate,
		location : location
	};
	console.log(event_data);

	var ajax = $.ajax({
		type : "POST",
		url : "/CreateQuizHandler",
		context : this,
		data : { 'data' : JSON.stringify(event_data) },	
		cache : false,
		success: function(result) {
			alert(result);
			result = JSON.parse(result);
			window.location.replace("/ModifyQuiz?id=" + result.id);
		}
	});
}

function SendModifyEventData() {
	var id = $("#input-id").val();
	var title = $("#input-title").val();
	var description = $("#input-description").val();
	var startdate = $("#input-startdate").val();
	var enddate = $("#input-enddate").val();
	var location = $("#input-location").val();
	event_data = {
		id : id,
		title : title,
		description : description, 
		startdate : startdate,
		enddate : enddate,
		location : location
	};
	console.log(event_data);

	var ajax = $.ajax({
		type : "POST",
		url : "/ModifyQuizHandler",
		context : this,
		data : { 'data' : JSON.stringify(event_data) },	
		cache : false,
		success: function(result) {
			alert(result);
			result = JSON.parse(result);
			window.location.replace("/ModifyQuiz?id=" + result.id);
		}
	});
}

function SendQuestionData() {
	question_data = [];
	$(".inputQuestion").each(function() {
		var topic = $(this).attr("topic");
		var ans_data = [];

		$(".answer-section[topic='" + topic + "'] .input_answer").each(function() {
			var istrue = $(this).find('input[type="checkbox"]').is(":checked");
			var ans = $(this).find('input[type="text"]').val();
			var ans_row = {
				answer : ans,
				istrue : istrue
			};
			ans_data.push(ans_row);
		});
		var question_val = $(this).val();
		if(!(question_val == null && question_val == "")) {
			var question = {
				question : $(this).val(),
				answer : ans_data,
			}
			question_data.push(question);
		}
	});
	console.log(JSON.stringify(question_data));

	var ajax = $.ajax({
		type : "POST",
		url : "...",
		context : this,
		data : JSON.stringify(question_data),	
		cache : false,
		success: function(result) {
			alert(result);
		}
	});
}