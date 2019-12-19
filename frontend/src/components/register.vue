<template>
    <div class="register1">
      <div class="header">
        <div class="header-left">
          <img src="../static/img/timg.jpg">
          <span>大学生赛事平台</span>
        </div>
        <div class="header-right">
          <!--<el-button type="text" @click="gotoIndex"><span>返回首页</span></el-button>-->
          <i class="el-icon-s-promotion"></i>
          <router-link :to="{ path: '/'}" replace><span>返回首页</span></router-link>
        </div>
      </div>
      <div class="register-body">
        <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm"  class="demo-ruleForm">
          <el-form-item label="" prop="username">
            <el-input v-model="ruleForm.username" clearable placeholder="用户名"></el-input>
          </el-form-item>
          <el-form-item label="" prop="email">
            <el-input v-model="ruleForm.email" clearable placeholder="邮箱"></el-input>
          </el-form-item>
          <el-form-item label="" prop="pass">
            <el-input type="password" v-model="ruleForm.pass" autocomplete="off" placeholder="密码" clearable></el-input>
          </el-form-item>
          <el-form-item label="" prop="pass_check">
            <el-input type="password" v-model="ruleForm.pass_check" autocomplete="off" placeholder="确认密码" clearable></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')">
              注册
            </el-button>
          </el-form-item>
        </el-form>
        <p class='login1'><router-link to='/login'>已注册？去登录</router-link></p>
      </div>
    </div>
</template>

<script>
    export default {
        name: "register",
      data(){
        var checkEmail = (rule, value, callback) => {
          var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$");
          if (!value) {
            return callback(new Error('邮箱不能为空'));
          }
          setTimeout(() => {
            if (!reg.test(value)) {
              callback(new Error('请输入正确的邮箱'));
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

        var validatePass2 = (rule, value, callback) => {
          if (value === '') {
            callback(new Error('请再次输入密码'));
          } else if (value !== this.ruleForm.pass) {
            callback(new Error('两次输入密码不一致!'));
          } else {
            callback();
          }
        };

        var checkUserName = (rule, value, callback) => {
          let reg =  /^[a-zA-Z0-9]{5,10}$/;
          if (!value) {
            return callback(new Error('用户名不能为空'));
          }
          setTimeout(() => {
            if (!reg.test(value)) {
              callback(new Error('用户名长度需5-10位，只可由字母与数字组成'));
            }else{
              callback();
            }
          }, 1000);
        };
          return {
            ruleForm:{
              email:'',
              username:null,
              pass:'',
              pass_check:''
            },
            rules:{
              pass: [
                { validator: validatePass, trigger: 'blur' }
              ],
              pass_check: [
                { validator: validatePass2, trigger: 'blur' }
              ],
              email: [
                { validator: checkEmail, trigger: 'blur' }
              ],
              username:[
                {validator: checkUserName, trigger: 'blur'}
              ]
            },
          }
      },
      methods:{
          gotoIndex() {
            this.$router.push('/')
          },
        submitForm(formName) {
          this.$refs[formName].validate((valid) => {
            if (valid) {
              this.$api.user.register({
                username:this.ruleForm.username,
                password:this.ruleForm.pass,
                email:this.ruleForm.email
              }).then((res)=>{
                  if(res.data.status==0){
                    this.$message.success('注册成功，赶紧登录吧！')
                    this.$router.push('/login')
                  }else {
                    this.$message.error(res.data.message);
                  }
                }
              )
            } else {
              this.$message.error('请正确完善注册信息');
            }

          })

        },
      }
    }
</script>

<style lang="scss">
  .register1{
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
    .register-body{
      margin-top:200px;
      width:50%;
      margin-left:25%;
      .el-input__inner{
        border-radius:30px;
      }
      .el-button{
        border-radius:30px;
        width:100%;
      }
      .login1{
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
    }
  }

</style>
