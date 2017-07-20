%#print('Im in gantt------------------------------------')
<!DOCTYPE html>
<html  class="no-js" lang="pt-PT">
  <head>
    <meta charset="utf-8">
    <title>Gráfico de Gantt</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Plano de Atividades - Gráfico de Gantt">
    <meta name="author" content="António Anacleto">
    <link href="/mfptask/static/css/d3.css" rel="stylesheet" />
    <link href="/mfptask/static/css/d3_erp.css" rel="stylesheet" />

    <link rel="shortcut icon" href="/mfptask/static/favicon.png">
    <script src="/mfptask/static/js/modernizr.js"></script>
  </head>
  <body>
    <input type="hidden" name="gantt_type" id="gantt_type" value="{{gantt_type}}">
    <input type="hidden" name="gantt_value" id="gantt_value" value="{{gantt_value}}">
    <input type="hidden" name="gantt_state" id="gantt_state" value="{{gantt_state}}">
    <div>
        <button type="button" onclick="changeTimeDomain('1Semana')">Semana</button>
        <button type="button" onclick="changeTimeDomain('1Mes')">Mês</button>
        <button type="button" onclick="changeTimeDomain('1Trimestre')">Trimestre</button>
        <button type="button" onclick="changeTimeDomain('1Semestre')">Semestre</button>
        <button type="button" onclick="changeTimeDomain('1Ano')">Ano</button>        
        <div id="gantt_div"></div>
    </div>
    </body>
    </html>
    <script src="/mfptask/static/js/jquery.min.js"></script>
    <script src="/mfptask/static/js/d3.min.js"></script>
    <script src="/mfptask/static/js/gantt-chart.js"></script>
    <script>

var taskStatus = {
    "Aberto" : "bar-aberto",
    "Resolvido" : "bar-resolvido",
    "Em Execução" : "bar-em_execucao",
    "Cancelado" : "bar-cancelado",
    "Para Acordo": "bar-para_acordo",
    "Executado": "bar-executado",
    "Pendente": "bar-pendente",
    "Datas Acordadas": "bar-datas_acordadas",
    "Previsional": "bar-previsional"
};

var tasks = {{!tasks}};
var taskNames = {{!taskNames}};

$.each(tasks, function() {
    this['startDate'] = new Date(this['startDate']);
    this['endDate'] = new Date(this['endDate']);
});


var maxDate = Date.now() + 31;
var minDate = Date.now();
var format = "%d/%m";
var timeDomainString = "1Mes";
var gantt = d3.gantt();
gantt.timeDomainMode("fixed");

var gantt_height = taskNames.length * 20;
if (taskNames.length == 1){
    gantt_height =  70;
};

gantt.tickFormat(format).height(gantt_height).width(900);

tasks.sort(function(a, b) {
    return a.endDate - b.endDate;
});

var maxDate = tasks[tasks.length - 1].endDate;
tasks.sort(function(a, b) {
    return a.startDate - b.startDate;
});

var minDate = tasks[0].startDate;
gantt.taskTypes(taskNames).taskStatus(taskStatus);
changeTimeDomain(timeDomainString);
gantt(tasks);

function changeTimeDomain(timeDomainString) {
    this.timeDomainString = timeDomainString;
    switch (timeDomainString) {
 
    case "1dia":
    format = "%H:%M";
    gantt.timeDomain([ getStartDate(), d3.time.day.offset(getStartDate(), +1) ]);
    break;

    case "1Semana":
    format = "%d/%m";
    gantt.timeDomain([ getStartDate(), d3.time.day.offset(getStartDate(), +7) ]);
    break;

    case "1Mes":
    format = "%d/%m";
    gantt.timeDomain([ getStartDate(), d3.time.day.offset(getStartDate(), +31) ]);
    break;

    case "1Trimestre":
    format = "%d/%m";
    gantt.timeDomain([ getStartDate(), d3.time.day.offset(getStartDate(), +93) ]);
    break;

    case "1Semestre":
    format = "%m/%y";
    gantt.timeDomain([ getStartDate(), d3.time.day.offset(getStartDate(), +193) ]);
    break;

    case "1Ano":
    format = "%m/%y";
    gantt.timeDomain([ getStartDate(), d3.time.day.offset(getStartDate(), +386) ]);
    break;

    default:
    format = "%H:%M"

    }
    gantt.tickFormat(format);
    gantt.redraw(tasks);
}

function getEndDate() {
    var lastEndDate = Date.now();
    if (tasks.length > 0) {
    lastEndDate = tasks[tasks.length - 1].endDate;
    }

    return lastEndDate;
}

function getStartDate() {
    var lastStartDate = Date.now();
    //if (tasks.length > 0) {
    //lastStartDate = tasks[tasks.length - 1].startDate;
    //}
    return lastStartDate;
}

</script>