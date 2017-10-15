

(function (jq) {


    var requesturl='';

    var GLOBAL_CHOICES_DICT={};

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

                    /*这是一个都选框功能*/
                    bindcheckout(response.search_config,response.global_choices_dict)

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
    
    function bindcheckout(search_config,global_choices_dict) {
        var status_choices=global_choices_dict.status_choices;
        var search_config=search_config;
        $('#tBody').on('click','.checkbox',function () {
            if(!$(this).attr('checked')){
                $(this).attr('checked','checked');
                $(this).parent().nextAll().each(function () {
                    if ($(this).attr('class') !='c1' ){
                        if($(this).attr('type') == 'input'){
                            var text = $(this).text();
                            $(this).html('<input class="form-control no-radius" value='+ text +'></input>');
                        }else if($(this).attr('type') == 'select'){
                            var tag=document.createElement('select');
                            tag.className="form-control no-radius";
                            var option_id=$(this).attr('option_id');
                            $.each(status_choices,function (k,v) {
                                var op=document.createElement('option') ;
                                op.innerHTML=v[1] ;
                                op.setAttribute('value',v[0]);
                                if(v[0] == option_id){
                                    op.setAttribute('selected','selected')
                                }
                                $(tag).append(op);
                            });
                            $(this).html(tag)
                        }
                    }
                })
            }else{
                $(this).removeAttr('checked');
                $(this).parent().nextAll().each(function () {
                    if($(this).attr("type") == "input"){
                        var val=$(this).find('input').val();
                        $(this).empty();
                        $(this).text(val)
                    }else if($(this).attr("type") == "select"){
                        var val=$(this).find('select').val();
                        var $this=$(this);
                        $(this).empty();
                        $.each(status_choices,function (k,v) {
                            if (val ==v[0]){
                                $this.attr('option_id' ,v[0]);
                                $this.text(v[1]);
                            }
                        })
                    }
                })
            }
        })
    }

    jq.extend({
        'nBList':function (url) {
            requesturl=url;
            init(1);
            /*包含一些修改名称的设置*/
            bindSearchConditionEvent()
        },
        'changePage':function (pageNum) {
            init(pageNum)
        }
    })

})(jQuery);