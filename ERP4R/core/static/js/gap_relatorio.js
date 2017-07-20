    function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
                color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    function hexToRgb(hex) {
            var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }

    //essa funçao vai dar cores aos serviços
    function giveColor(){
          var count = $("#servicesize").val();
          var color;
          var colorContent = [];
          for(var i=0;i<count;i++){
                while(true){
                    color = getRandomColor();
                    if(color!="#FFFFFF" ||  color!="#FFF"){
                        if(!checkColor(color,colorContent)){
                            colorContent.push(color);
                            break;
                        }
                    }
                }
                $("#service"+i).css('background-color', color);
          }
          return colorContent;
    }

    //essa funçao vai verificar se a cor gerada nao esta a ser utilizada
    function checkColor(color,colorContent){
        for (var i =0; i<colorContent.length; i++) {
                    if(color == colorContent[i]){
                            return true;
                    }
        };
        return false;
    }