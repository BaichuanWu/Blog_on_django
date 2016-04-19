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
                    var temp = "<lable><h5 class='inline'>"+v.user__user__username+":</h5>&nbsp;&nbsp;"+
                        v.content+"</lable><span class='inline right-float date-grey'>"+
                        v.create_date+"</span><hr class='reply'/>";
                    $(content).parent().parent().next().find('.rep-node').append(temp);

                });
            }
        }
    );
    $(content).parent().parent().next().toggleClass('hide');

}

function addReply(content, id) {
    var reply_content = $(content).prev().val();
    $.ajax({
        url:'/blog/addreply/',
        data:{nid:id, data:reply_content},
        type:'POST',
        success:function (calback) {
            // console.log(calback);
            var temp = "<lable><h5 class='inline'>"+calback.user+":</h5>&nbsp;&nbsp;"+
                        calback.content+"</lable><span class='inline right-float date-grey'>"+
                        calback.create_date+"</span><hr class='reply'/>";
            $(content).parent().prev().append(temp);
            $(content).prev().val('');
            console.log(calback.count);
            console.log($(content).parent().parent().prev().find('span.fav')[0].innerHTML);
            $(content).parent().parent().prev().find('span.fav')[0].innerHTML=calback.count

        }

    })

}
