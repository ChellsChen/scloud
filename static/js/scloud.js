/**
 *
 * @authors 陈小雪 (shell_chen@yeah.net)
 * @date    2015-09-22 17:18:05
 * @version $Id$
 */

var tomarked = function(){
    var markstr = $("#markdown-text").val();
    $(".content").html(marked(markstr));
}

function save_md(){
    var md_tex = $("#markdown-text").val();
    var html_tex = $(".content").html();
    var id = localStorage.getItem("id");
    var post = 1;
    if(document.getElementById("md-post").checked){
        post = 0;
    }
    if (!id){
        return;
    }

    var data = {
        id: id,
        md:md_tex,
        html: html_tex,
        post:post,
    };

    $.ajax({
        url: "/mdeditor/",
        method: "put",
        dataType: "json",
        data: data,
        success:function(data){
            if(data.status != 0){
                layer.alert(data.message);
            }
        }
    });

}

function new_md(){
    $.ajax({
        url:"/mdeditor/",
        dataType: "json",
        method:"post",
        success:function(data){
            layer.close($(".new-tex")[0]._data);
            localStorage.setItem("id", data.id);
            window.location.href="/mdeditor?id="+data.id;
        }
    });
}

function delete_md() {
    var id = localStorage.getItem("id");
    $.ajax({
        url:"/mdeditor/?id="+ id,
        dataType:"json",
        method:"delete",
        success:function(data){

        }
    })
}


function  GetUrlParams () {
    var reslut = { };
    var params = (window.location.search.split("?")[1] || "").split("&");
    for (var param in params)
    {
        if(params.hasOwnProperty(param))
        {
            paramParts = params[param].split("=");
            reslut[paramParts[0]] = decodeURIComponent(paramParts[1] || "");

        }
    }
    return reslut;
}


