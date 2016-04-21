/**
 * Created by alian on 16/4/13.
 */

function reply(content, id) {
    $(content).parent().parent().next().find('.rep-node').empty();
    $.ajax({
            url: '/blog/getreply/',
            data: {nid: id},
            type: 'POST',
            success: function (calback) {
                console.log(calback);
                $.each(calback, function (k,v) {
                    var temp = "<lable><h5 class='inline'>"+v.user__user__username+
                        ":</h5>&nbsp;&nbsp;&nbsp;</lable><span class='inline right-float date-grey'>"+
                        v.create_date+"</span>"+
                        v.content+"<hr class='reply'/>";
                    $(content).parent().parent().next().find('.rep-node').append(temp);

                });
            }
        }
    );
    $(content).parent().parent().next().toggleClass('hide');

}

function addReply(content, id) {
    var reply_content = $(content).prev().val();
    if (!reply_content){
        console.log($(content).next());
        $(content).next().removeClass('hide');
    }
    else {
        $.ajax({
            url:'/blog/addreply/',
            data:{nid:id, data:reply_content},
            type:'POST',
            success:function (calback) {
                // console.log(calback);
                var temp = "<lable><h5 class='inline'>"+calback.user+
                    ":</h5>&nbsp;&nbsp;</lable><span class='inline right-float date-grey'>"+
                    calback.create_date+"</span>"+calback.content+"<hr class='reply'/>";
                $(content).parent().prev().append(temp);
                $(content).prev().val('');
                $(content).parent().parent().prev().find('span.fav')[0].innerHTML=calback.count
            }
        })
    }
}

function addMessage(content, id) {
    var reply_content = $(content).prev().val();
    if (!reply_content){
        console.log($(content).next());
        $(content).next().removeClass('hide');
    }
    else {
        $.ajax({
            url:'/blog/add_message/',
            data:{data:reply_content},
            type:'POST',
            success:function (calback) {
                var temp = "<div class='message'><a href='/blog/profile/"+calback.id+"'><h4 class='inline'>"
                    +calback.user+":</h4></a>&nbsp;&nbsp;&nbsp;"+
                    "</lable><span class='inline right-float date-grey'>"+
                    calback.create_date+"</span>"+
                    calback.content+"<hr class='reply'/></div>";
                $(content).parent().prev().append(temp);
                $(content).prev().val('');
            }
        })
    }
}

function validatePsw() {
    var psw1 = document.getElementById('psw1').value;
    var psw2 = document.getElementById('psw2').value;
    console.log(psw1, psw2);
    if (psw1 == psw2) {
        document.getElementById('conf').innerHTML = '<p class="bg-success bar">密码相同</p>';
        document.getElementById('submit').disabled = false;
    }
    else {
        document.getElementById('conf').innerHTML = '<p class="bg-warning bar">密码不同</p>';
        document.getElementById('submit').disabled = true;
    }
}

function validateName(content) {
    var temp =$(content).val();
    console.log(2<temp.length && temp.length<13);
    if (2<temp.length && temp.length<13) {
        $.ajax({
            url: '/blog/confirm/',
            data: {nid: temp},
            type: 'POST',
            success: function (calback) {
                if (calback.name) {
                    document.getElementById('n-conf').innerHTML = '<p class="bg-success bar">用户名可用</p>';
                }
                else {
                    document.getElementById('n-conf').innerHTML = '<p class="bg-warning bar">用户名重复</p>';
                }
            }
        })
    }else {
        document.getElementById('n-conf').innerHTML = '<p class="bg-warning bar">用户名格式不符</p>';
    }
}