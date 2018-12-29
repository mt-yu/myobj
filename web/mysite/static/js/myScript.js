function add_column() {
    var index = layer.open({
        type: 1,
        skin: "layui-layer-rim",
        area: ["400px", "200px"],
        title: "新增栏目",
        content: '<div class="text-center" style="margin-top:20px"><p> 请输入新的栏目名称</p><p>' +
            columnVar.a + '</p></div > ',
        btn: ['确定', '取消'],
        yes: function (index, layero) {
            column_name = $('#id_column').val();
            $.ajax({
                url: columnVar.b,
                type: 'POST',
                data: { "column": column_name },
                success: function (e) {
                    if (e == "1") {
                        parent.location.reload();
                        layer.msg("good");
                    } else {
                        layer.msg("此栏目已有，请更换名称")
                    }
                },
            });
        },
        btn2: function (index, layero) {
            layer.close(index);
        }
    });
}

function edit_column(the, column_id){
    var name = $(the).parents("tr").children("td").eq(1).text();
    var index = layer.open({
        type: 1,
        skin: "layui-layer-rim",
        area: ["400px", "200px"],
        title: "编辑栏目",
        content: '<div class="text-center" style="margin-top:20px"><p>请编辑的栏目名称</p><p><input type="text" id="new_name" value="'+name+'"></p></div>',
        btn:['确定', '取消'],
        yes: function(index, layero){
            new_name = $("#new_name").val();
            $.ajax({
                url: columnVar.c,
                type: "POST",
                data: {"column_id": column_id, "column_name": new_name},
                success: function(e){
                    if(e=="1"){
                        parent.location.reload();
                        layer.msg("good");
                    }else{
                        layer.msg("新的名称没有保存,修改失败。")
                    }
                },
            });
        },
    });
}

function del_column(the, column_id){
    var name = $(the).parents("tr").children("td").eq(1).text();
    layer.open({
        type: 1,
        skin: "layui-layer-rim",
        area: ["400px", "200px"],
        title: "删除栏目",
        content: '<div class="text-center" style="margin-top:20px"><p>是否确定删除{'+name+'}栏目</p> </div>',
        btn:['确定', '取消'],
        yes: function(){
            $.ajax({
                url: columnVar.d,
                type: "POST",
                data: {"column_id":column_id},
                success: function(e){
                    if(e=="1"){
                        parent.location.reload();
                        layer.msg("has been deleted.");
                    }else{
                        layer.msg("删除失败");
                    }
                },
            })
        },
    });
}