<template>
    <div class="login">
      <div class="header">
        <div class="header-left">
          <img src="../static/img/com.jpg">
          <span>京西电脑商城</span>
        </div>
        <div class="header-right">
          <!--<el-button type="text" @click="gotoIndex"><span>返回首页</span></el-button>-->
          <i class="el-icon-s-promotion"></i>
          <router-link :to="{ path: '/'}" replace><span>返回首页</span></router-link>
        </div>
      </div>
      <div class="login-body">
        <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm"  class="demo-ruleForm">
          <el-form-item label="" prop="username">
            <el-input v-model="ruleForm.username" clearable placeholder="用户名/邮箱"></el-input>
          </el-form-item>
          <el-form-item label="" prop="pass">
            <el-input type="password" v-model="ruleForm.pass" autocomplete="off" placeholder="密码" clearable></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')">
              登录
            </el-button>
          </el-form-item>
        </el-form>
        <p class='register'><router-link to='/register'>还没账号？去注册</router-link></p>
      </div>
    </div>
</template>

<script>
    export default {
        name: "login",
      data(){
        var checkAccount = (rule, value, callback) => {
          var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$");
          var regNum = /^[a-zA-Z0-9]{5,10}$/;;
          if (!value) {
            return callback(new Error('邮箱或用户名不能为空'));
          }
          setTimeout(() => {
            if (!reg.test(value) && !regNum.test(value)) {
              callback(new Error('请输入正确的邮箱或用户名'));
            }else{
              callback();
            }
          }, 1000);
        };

        var validatePass = (rule, value, callback) => {
          let reg = /(?!^[0-9]+$)(?!^[A-z]+$)(?!^[^A-z0-9]+$)^[^\s\u4e00-\u9fa5]{6,16}$/;
          if (value === '') {
            callback(new Error('请输入密码'));
          }else if(!reg.test(value)){
            callback(new Error('密码长度需6-16位，且包含字母和字符'))
          } else {
            if (this.ruleForm.pass_check !== '') {
              this.$refs.ruleForm.validateField('pass_check');
            }
            callback();
          }
        };
          return{
            rules:{
              username:[
                {validator: checkAccount, trigger: 'blur'}
              ],
              pass:[
                {validator: validatePass, trigger: 'blur'}
              ]
            },
            ruleForm:{
              username:'',
              pass:''
            },
            username:'',
            nickName:'',
            userId:'',
          }
      },
      methods:{
          gotoIndex(){
            this.$router.push('/')
          },
        submitForm(formName) {
          this.$refs[formName].validate((valid) => {
            if (valid) {
              this.$api.user.login({
                username:this.ruleForm.username,
                password:this.ruleForm.pass,
              }).then((res)=>{
                  if(res.data.status=='0'){
                    console.log(res)
                    let info = res.data
                    let userId = info['id']
                    sessionStorage.setItem('userId', userId)
                    let username = info['username']
                    sessionStorage.setItem('username', username)
                    let nickName = info['Unickname']
                    sessionStorage.setItem('nickName', nickName)
                    let email = info['email']
                    sessionStorage.setItem('email', email)
                    let imgurl = info['img']
                    sessionStorage.setItem('imgurl', imgurl)
                    let is_superuser = info['is_superuser']
                    sessionStorage.setItem('is_superuser', is_superuser)
                    this.$message.success('登录成功！')
                    this.$router.push('/')
                  }else {
                    this.$message.error("用户名/邮箱或密码错误，请重试！");
                  }
                }
              )
            } else {
              this.$message.error('请正确填写登录信息！');
            }

          })

        },
      }
    }
</script>

<style lang="scss">
  .header{
    position: fixed;
    left:0px;
    top:0px;
    background-color: #f7f7f7;
    width:100%;
    height:100px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    .header-right{
      height:100%;
      width:20%;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      span{
        color:#2C537A
      }
      a {
        text-decoration: none;
      }
    }
    .header-left{
      height:100%;
      width:30%;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-around;
      img{
        width:110px;
        height:94%;
        margin-top:3%;
        margin-bottom:3%;
      }
      span{
        font-size:32px;
      }
    }
  }
  .login-body{
    margin-top:200px;
    width:50%;
    margin-left:25%;
    .register {
      text-align: right;
      margin: 10px;
      float:right;
      width:46%;
      a {
        //     color: #f3a407
        color:#409eff;
        text-decoration:none
      }
    }
    .el-form{
      width:100%;
      margin-left:0%;
      .el-input__inner{
        border-radius:30px;
      }
      .el-button{
        width:100%;
        border-radius:30px;
      }
    }
  }
</style>
