<template>
    <div class="center-container">
    <div class="ticket">
        <div class="stub">
            <div class="top">
                <span class="admit">Admit</span>
                <span class="line"></span>
                <span class="num">
                    Invitation
                    <span>31415926</span>
                </span>
            </div>
            <div class="number"></div>
            <div class="invite">
                Invite for you
            </div>
        </div>
        <div class="check">
            <div class="big">
                You're <br> Invited
            </div>
            <div class="number">#1</div>
            <div class="info">
                <section>
                    <div class="title">Date</div>
                    <div>4/27/2016</div>
                </section>
                <section>
                    <div class="title">Issued By</div>
                    <div>Ampersand</div>
                </section>
                <section>
                    <div class="title">Invite Number</div>
                    <div>31415926</div>
                </section>
            </div>
        </div>
    </div>
</div>
</template>

<script>
export default {

}
</script>

<style scoped>

.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh; 
}
.ticket {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 700px;
    margin: 20px auto;
}

.ticket .stub,
.ticket .check {
    box-sizing: border-box;
}

.stub {
    background: #6a80eb;
    height: 250px;
    width: 250px;
    color: white;
    padding: 20px;
    position: relative;
}

.stub:before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    border-top: 20px solid #a7c0df;
    border-left: 20px solid #6a80eb;
    width: 0;
}

.stub:after {
    content: '';
    position: absolute;
    bottom: 0;
    right: 0;
    border-bottom: 20px solid #a7c0df;
    border-left: 20px solid #6a80eb;
    width: 0;
}

.stub .top {
    display: flex;
    align-items: center;
    height: 40px;
    text-transform: uppercase;
}

.stub .top .line {
    display: block;
    background: #fff;
    height: 40px;
    width: 3px;
    margin: 0 20px;
}

.stub .top .num {
    font-size: 10px;
}

.stub .top .num span {
    color: #000;
}

.stub .number {
    position: absolute;
    left: 40px;
    font-size: 150px;
}

.stub .invite {
    position: absolute;
    left: 150px;
    bottom: 45px;
    color: #000;
    width: 20%;
}

.stub .invite:before {
    content: '';
    background: #fff;
    display: block;
    width: 40px;
    height: 3px;
    margin-bottom: 5px;
}

.check {
    background: #fff;
    height: 250px;
    width: 450px;
    padding: 40px;
    position: relative;
}

.check:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    border-top: 20px solid #a7c0df;
    border-right: 20px solid #fff;
    width: 0;
}

.check:after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    border-bottom: 20px solid #a7c0df;
    border-right: 20px solid #fff;
    width: 0;
}

.check .big {
    font-size: 80px;
    font-weight: 900;
    line-height: .8em;
}

.check .number {
    position: absolute;
    top: 50px;
    right: 50px;
    color: #6a80eb;
    font-size: 40px;
}

.check .info {
    display: flex;
    justify-content: flex-start;
    font-size: 12px;
    margin-top: 20px;
    width: 100%;
}

.check .info section {
    margin-right: 50px;
}

.check .info section:before {
    content: '';
    background: #6a80eb;
    display: block;
    width: 40px;
    height: 3px;
    margin-bottom: 5px;
}

.check .info section .title {
    font-size: 10px;
    text-transform: uppercase;
}</style>