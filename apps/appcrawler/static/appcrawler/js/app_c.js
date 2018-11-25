/**
 * Created by yyfaxx on 2018/7/9.
 */
//后门杀手锏
// $(document).on('click', "#fycstop", function () {
//     var udid = $("#fycudid").val();
//     $.ajax({
//         url: '/appcrawler/stopMinicap',
//         type: 'GET',
//         datatype: 'json',
//         data: {'udid': udid}
//     }).done(function (data) {
//         if (data.data == 'True') {
//             PassAlert('关闭成功');
//             //$("#frameHere").empty();
//             //$("#AppiumMessage").empty();
//         } else if (data.data == 'False') {
//             WarningAlert('关闭失败！请重新点击关屏！');
//         } else if (data.data == 'Error') {
//             ErrorAlert('系统错误，请联系管理员!!')
//         }
//     });
// });
// $(document).on('click', "#fycstopall", function () {
//     $.ajax({
//         url: '/appcrawler/stopServer',
//         type: 'GET',
//         datatype: 'json',
//         beforeSend: function () {
//             PassAlert('全部干掉了...所有的...');
//         }
//     })
// });

$(document).on("click", ".btn-xs", function () {
    var cls = $(this).attr('class');
    var udid = $(this).parent("td").attr("id");
    if (cls == 'btn btn-primary btn-xs') {
        $.ajax({
            url: '/appcrawler/runAppiumSigle',
            type: 'GET',
            datatype: 'json',
            data: {'udid': udid}
        }).done(function (data) {
            if (data.data == 'False') {
                WarningAlert('Appium进程已启动，请勿重复启动！')
            } else {
                PassAlert('正在启动，请稍候。。')
            }
        })
    } else if (cls == 'btn btn-warning btn-xs') {
        $.ajax({
            url: '/appcrawler/stopAppiumSigle',
            type: 'GET',
            datatype: 'json',
            data: {'udid': udid}
        }).done(function (data) {
            if (data.data == 'True') {
                PassAlert('Appium终止成功')
            } else if (data.data == 'False') {
                WarningAlert('未找到指定Appium进程，应该不存在此进程')
            } else {
                ErrorAlert('系统错误！请联系管理员')
            }
        })
    } else if (cls == 'btn btn-default btn-xs') {
        var htmlUDID = $("iframe").attr('name');
        if (typeof(htmlUDID) == 'undefined') {
            $.ajax({
                url: '/appcrawler/startMinicap',
                type: 'GET',
                datatype: 'json',
                data: {'udid': udid, 'test': 'True'}
            }).done(function (data) {
                if (data.data == 'False') {
                    WarningAlert('该设备投屏已被其他人占用，请更换设备使用！');
                } else {
                    $.ajax({
                        url: '/appcrawler/startMinicap',
                        type: 'GET',
                        datatype: 'json',
                        data: {'udid': udid, 'test': 'False'},
                        beforeSend: function () {
                            $('#AlertTitle').html('<h3>提示</h3>');
                            $('#msg').html('稍候，不要刷新页面，马上就好');
                            $('#myModal').modal('show');
                        }
                    }).done(function (data) {
                        $('#myModal').modal('hide');
                        if (data.data == 'True') {
                            $("#AppiumMessage").empty();
                            $("#AppiumMessage").html("正在控制：" + data.name);
                            // var lens = $("#AppiumTbody").find("tr").length;
                            // for(var i=0;i<lens;i++)
                            // {
                            //     var mes = $("#AppiumTbody").children('tr').eq(i+1).children('td').eq(i+1).text();
                            //     alert(mes);
                            //     if (mes == data.name){
                            //         $("#AppiumTbody").children('tr').eq(i+1).addClass('class="warning"')
                            //     }
                            // }
                            $("#frameHere").empty();
                            $("#frameHere").html('<iframe src="appcrawler/minicapView?PORT=' + data.port + '&touch=' + data.touchPort + '&mtsp=' + data.mtsp + '&udid=' + data.udid + '" name="' + data.udid + '" scrolling="no" frameborder="0" id="myframe" style="width: 900px; height: 900px;"></iframe>')

                        } else {
                            ErrorAlert('系统错误，请联系管理员')
                        }
                    })
                }
            })
        } else {
            WarningAlert('已有投屏啦，不要重复打开了！')
        }

    } else if (cls == 'btn btn-danger btn-xs') {
        var htmlUDID = $("iframe").attr('name');
        var mod = $("#tagadmin").text();
        if (htmlUDID == udid || mod == 'Admin') {
            $.ajax({
                url: '/appcrawler/stopMinicap',
                type: 'GET',
                datatype: 'json',
                data: {'udid': udid}
            }).done(function (data) {
                if (data.data == 'True') {
                    PassAlert('关闭成功');
                    $("#frameHere").empty();
                    $("#AppiumMessage").empty();
                    $("#AppiumMessage").html('<span style="color: red;">用完请及时关闭投屏，以免影响其他人使用！！</span>');
                } else if (data.data == 'False') {
                    WarningAlert('关闭失败！请重新点击关屏！');
                } else if (data.data == 'Error') {
                    ErrorAlert('系统错误，请联系管理员!!')
                }
            })
        } else if (typeof(htmlUDID) == 'undefined') {
            WarningAlert("大哥，你要先开启一个投屏才可以关闭啊，你说对不对？")
        } else {
            WarningAlert("我说。。你不要关闭其他人的投屏，别这么搞，不合适。。")
        }

    }

});

function PassAlert(msg) {
    $('#AlertTitle').html('<span class="am-icon-btn am-success am-icon-check"></span>');
    $('#msg').html(msg);
    $('#myModal').modal('show');
    setTimeout(function () {
        $("#myModal").modal("hide");
        $('#AlertTitle').empty();
        $('#msg').empty()
    }, 1000);
}
function WarningAlert(msg) {
    $('#AlertTitle').html('<span class="am-icon-btn am-warning am-icon-warning"></span>');
    $('#msg').html(msg);
    $('#myModal').modal('show');
    setTimeout(function () {
        $("#myModal").modal("hide");
        $('#AlertTitle').empty();
        $('#msg').empty()
    }, 1000);
}
function ErrorAlert(msg) {
    $('#AlertTitle').html('<span class="am-icon-btn am-danger am-icon-remove"></span>');
    $('#msg').html(msg);
    $('#myModal').modal('show');
    setTimeout(function () {
        $("#myModal").modal("hide");
        $('#AlertTitle').empty();
        $('#msg').empty()
    }, 1000);
}
