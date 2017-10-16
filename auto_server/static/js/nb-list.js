

(function (jq) {


    var requesturl='';

    var GLOBAL_CHOICES_DICT={};

    /*请求头的添加*/
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // 请求头中设置一次csrf-token
            if(!csrfSafeMethod(settings.type)){
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });
    /*请求头的添加完成*/

    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };


    function init(pageNum) {

        // var condition=;

        $.ajax(
            {
                url:requesturl,
                type:'GET',
                data:{'pageNum':pageNum,'condition':JSON.stringify(getSearchCondition())},
                dataType:"JSON",
                success:function (response) {
                    /* 获取到了一个变量*/
                    GLOBAL_CHOICES_DICT=response.global_choices_dict;
                    /*制作一个表头*/
                    initTableHead(response.table_config);

                    /*制作一个表主体*/
                    initTableBody(response.data_list,response.table_config);
                    /*初始化一个搜索框*/
                    initSearchCondition(response.search_config);
                    /*分页功能*/
                    pageinhtml(response.page_html);


                }
            }
        )
    }

    function initTableHead(table_config){
        /*          'q':'os_platform',
            'title':'系统',
            'display':True,
            'text':{'tpl':'{a1}','kwargs':{"a1":'@os_platform'}},
        },
        */
        $('#tHead tr').empty();
        $.each(table_config,function (k,conf) {
            if (conf.display){
                var th=document.createElement('th');
                th.innerHTML=conf.title;
                $('#tHead tr').append(th);
            }
        })
    }

    function initTableBody(date_list,table_config){
        $('#tBody').empty();
        $.each(date_list,function (k,row_dict) {
            var tr=document.createElement('tr');
            $.each(table_config,function (kk,vv) {
                if (vv.display){
                    var td=document.createElement('td');
                    var format_dict={};
                    $.each(vv.text.kwargs,function (kkk,vvv) {
                        if(vvv.substring(0,2)=="@@"){
                         var name = vvv.substring(2,vvv.length);
                         var status_choices_list=GLOBAL_CHOICES_DICT[name];
                         $.each(status_choices_list,function (kkkk,vvvv) {
                             if(row_dict[vv.q]==vvvv[0]){
                                 format_dict[kkk]=vvvv[1]
                             }
                         });
                        }
                        else if(vvv[0]=='@'){
                            var name = vvv.substring(1,vvv.length);
                            format_dict[kkk]=row_dict[name]
                        }else{
                            format_dict[kkk]=vvv;
                        }
                    });

                    td.innerHTML=vv.text.tpl.format(format_dict);
                    $.each(vv.attr,function (attrk,attrv) {     if(attrv[0] == "@"){
                        attrv= row_dict[attrv.substring(1,attrv.length)]
                    }
                    td.setAttribute(attrk,attrv)
                    });

                    $(tr).append(td);
                }
            });
            $('#tBody').append(tr);
        });
    }

    function initSearchCondition(searchconfig) {
        if(!$('#searchCondition').attr('init')){
            var $ul = $('#searchCondition :first').find('ul');
            $ul.empty();
                /*
                {
            'name':'hostname','title':'主机名','type':'input'
                 },
                */
                if(searchconfig[0].type == 'input'){
                    var tag = document.createElement('input');
                    tag.setAttribute('type','text');
                    tag.className='form-control no-radius';
                    tag.setAttribute('placeholder','请输入条件');
                    tag.setAttribute('name',searchconfig[0].name);
                }else{
                    var tag=document.createElement('select');
                    tag.className='form-control no-radius';
                    tag.setAttribute('name',searchconfig[0].name);
                    $.each(GLOBAL_CHOICES_DICT[searchconfig[0].choice_name],function (i,row) {
                        var op=document.createElement('option');
                        op.innerHTML=row[1];
                        op.setAttribute('value',row[0]);
                        $(tag).append(op);
                    });
                    }
                    $('#searchCondition').find('.input-group').append(tag)
                    $('#searchCondition').find('.input-group label').text(searchconfig[0].title);

            $.each(searchconfig,function (i,item) {
                var li = document.createElement('li');
                var a = document.createElement('a');
                a.innerHTML=item.title;
                a.setAttribute("name",item.name);
                a.setAttribute('type',item.type);
                if(item.type == 'select'){
                    a.setAttribute('choice_name',item.choice_name);
                }
                $(li).append(a);
                $ul.append(li);
            });
                $('#searchCondition').attr('init','true');
        }


    }

    function bindSearchConditionEvent(){
        /*改变了下拉框的内容时*/
        $('#searchCondition').on('click','li',function () {
            $(this).parent().prev().prev().prev().text($(this).text());
            /*查找到当前的ul标签然后把ul标签的内容给默认窗口覆盖上*/

            /* 找到后面输入框或者选择框*/
            $(this).parent().parent().next().remove();

            var name = $(this).find('a').attr('name');
            var type = $(this).find('a').attr('type');
            if(type == 'select'){
                var choice_name=$(this).find('a').attr('choice_name');

                var tag = document.createElement('select');
                tag.className="form-control no-radius";
                tag.setAttribute('name',name);
                $.each(GLOBAL_CHOICES_DICT[choice_name],function (i,item) {
                 var op=document.createElement('option') ;
                 op.innerHTML=item[1] ;
                 op.setAttribute('value',item[0]);
                 $(tag).append(op);
                })
            }else{
                var tag =document.createElement('input');
                tag.setAttribute('type','text');
                tag.className='form-control no-radius';
                tag.setAttribute('name',name);
                tag.setAttribute('placeholder','请输入条件');
            }
            $(this).parent().parent().after(tag)
        });

        /*添加新的条件*/
        $('#searchCondition').on('click','.add-condition',function () {
          var $cloneSearch=$(this).parent().parent().clone();
            $cloneSearch.find('.add-condition').removeClass('add-condition').addClass('del-condition').find('i').attr('class','fa fa-minus-square');
          $cloneSearch.appendTo($('#searchCondition'));
        });
        /*删除新的条件*/
        $('#searchCondition').on('click','.del-condition',function () {
           $(this).parent().parent().remove();
        });

        /*点击搜索键*/
        $('#doSearch').click(function () {
            init(1);
        })

    }

    function getSearchCondition(){
        console.log('bbbb ');
        var result={};
        $('#searchCondition').find('input[type="text"],select').each(function () {
            var name=$(this).attr('name');
            var val=$(this).val();
            console.log(val,'aaa ');
            if (result[name]){
                result[name].push(val)
            }else{
                result[name]=[val];
            }
        });
        return result;
    }

    function pageinhtml(page_html) {
        $('#pagination').empty().append(page_html)
    }

    
    function trIntoEditMode($tr) {
        $tr.addClass('success');
        $tr.find('td[edit="true"]').each(function () {
            tdIntoEditMode($(this));
        })
    }

    function tdIntoEditMode($td) {
        if($td.attr('edit-type') == 'select'){
            var choiceKey = $td.attr('choice-key');
            var origin = $td.attr('origin');
            var tag = document.createElement('select');
            tag.className='form-control';
            $.each(GLOBAL_CHOICES_DICT[choiceKey],function (k,value) {
                var op = document.createElement('option');
                op.innerHTML=value[1];
                op.value=value[0];
                if(value[0]==origin){
                    op.setAttribute('selected','selected');
                }
                tag.appendChild(op);
            });
            $td.html(tag);
        }else{
            var text=$td.text();
            var tag = document.createElement('input');
            tag.setAttribute('type','text');
            tag.className='form-control';
            tag.value = text;
            $td.html(tag);
        }
    }

    function trOutEditMode($tr) {
        $tr.removeClass('success');
        $tr.find('td[edit="true"]').each(function () {
            if (tdOutEditMode($(this))){
                $tr.attr('edit-status','true');
            }
        });
    }

    function tdOutEditMode($td) {
        var editStatus=false;
        var origin=$td.attr('origin');
        if($td.attr('edit-type')=='select'){
            var val=$td.find('select').val();
            var text = $td.find('select option[value="'+val+'"]').text();
            $td.attr('new-value',val);
            $td.html(text)
        }else{
            var val = $td.find('input').val();
            $td.html(val);
        }
        if(origin != val){
            editStatus = true;
        }
        return editStatus
    }

    function bindEditModeEvent() {
        $('#tBody').on('click',':checkbox',function () {
            if($('#editModeStatus').hasClass('btn-warning')){
                if($(this).prop('checked')){
                    var $tr = $(this).parent().parent();
                    $tr.addClass('success');
                    $tr.find('td[edit="true"]').each(function () {
                            tdIntoEditMode($(this));
                    });
                }else{
                    var $tr = $(this).parent().parent();
                    $tr.removeClass('success');
                    $tr.find('td[edit="true"]').each(function () {
            if(tdOutEditMode($(this))){
                $tr.attr('edit-status','true');
            }
                    });
                }
            }
        })
    }

    function bindBtnGroupEvent() {

        /*进入编辑和退出编辑模式*/
        $('#editModeStatus').click(function () {
            if ($(this).hasClass('btn-warning')) {
                $(this).removeClass('btn-warning');
                $(this).text('进入编辑模式');

                $('#tBody :checked').each(function () {
                    var $tr = $(this).parent().parent();
                    trOutEditMode($tr)
                })
            } else {
                $(this).addClass('btn-warning');
                $(this).text('退出编辑模式');
                $('#tBody :checked').each(function () {
                    var $tr = $(this).parent().parent();
                    trIntoEditMode($tr);
                })
            }
        });

        /*全选一下*/
        $('#checkAll').click(function () {
            $('#tBody :checkbox').each(function () {
                if (!$(this).prop('checked')) {
                    $(this).prop('checked', "true");
                    if ($('#editModeStatus').hasClass('btn-warning')) {
                        var $tr = $(this).parent().parent();
                        trIntoEditMode($tr)
                    }
                }
            });
        });
        
        /*取消一下下*/
        $('#checkCancel').click(function () {
            $('#tBody :checked').each(function () {
                $(this).prop('checked', false);
                if ($('#editModeStatus').hasClass('btn-warning')) {
                    var $tr = $(this).parent().parent();
                    trOutEditMode($tr)
                }
            })
        });
        
        /*反选*/
        $('#reverse').click(function () {
            $('#tBody :checkbox').each(function () {
                if(!$(this).prop('checked')){
                    //没被选中的孩子
                    $(this).prop('checked',true);
                    //进入编辑模式了么？
                    if ($('#editModeStatus').hasClass('btn-warning')){
                        var $tr = $(this).parent().parent();
                        trIntoEditMode($tr);
                    }
                }
                else{
                    $(this).prop('checked',false);
                    if($('#editModeStatus').hasClass('btn-warning')){
                        var $tr=$(this).parent().parent();
                        trOutEditMode($tr)
                    }
                }
            })
        });
        /*删除*/
        $('#delMulti').click(function(){
            $('#tBody :checkbox').each(function () {
                if($(this).prop('checked')){
                    $('#alertwarning').text('您真的要删除这些么');
                    $('#deleteether').attr('class','btn btn-primary');
                    return false
                }else{
                    $('#alertwarning').text('您还什么都没选呢');
                    $('#deleteether').attr('class','hide');
                }
            });
            $('#demoModal').modal('show');
        });

        /*确认删除*/
        $('#deleteether').click(function () {
            var ids=[];
            $('#tBody :checked').each(function () {
                ids.push($(this).val());
            });
            $.ajax(
                {
                    url:requesturl,
                    type:'delete',
                    data:JSON.stringify(ids),
                    traditional:true,
                    dataType:"JSON",
                    success:function (arg) {
                        if(arg.status){
                            $('#handleStatus').text('执行成功');
                            setTimeout(function () {
                                $('#handleStatus').empty()
                            },5000)
                        }else{
                            $('#handleStatus').text(arg.msg);
                        }
                    }
                }
            )
        })
    }
        /*保存*/
        $('#saveMulti').click(function () {
            if(!$('#editModeStatus').hasClass('btn-warning')){
                var update_dict=[]
            $('#tBody tr[edit-status="true"]').each(
                function () {
                    var tmp={};
                    tmp['id']= $(this).children().first().attr('nid');
                    $(this).children('[edit="true"]').each(
                        function () {
                            var origin=$(this).attr('origin');
                            var name=$(this).attr('name');
                            if($(this).attr('edit-type') == 'select'){
                                var newval=$(this).attr('new-value');
                            }else{
                                var newval=$(this).text()}
                                if (origin != newval){
                                tmp[name]=newval
                                }
                        });
                    update_dict.push(tmp);
                });
            $.ajax({
                url:requesturl,
                    type:'put',
                    data:JSON.stringify(update_dict),
                    traditional:true,
                    dataType:"JSON",
                    success:function (arg) {

                        if(arg.status){
                            $('#handleStatus').text('执行成功');
                            setTimeout(function () {
                                $('#handleStatus').empty()
                            },5000)
                        }else{
                            $('#handleStatus').text(arg.msg);
                        }
                    }
            })
            }

        });


    jq.extend({
        'nBList':function (url) {
            requesturl=url;
            init(1);
            /*包含一些修改名称的设置*/
            bindSearchConditionEvent();

            bindBtnGroupEvent();

            bindEditModeEvent();
        },
        'changePage':function (pageNum) {
            init(pageNum)
        }
    })

})(jQuery);