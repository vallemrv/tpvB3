(function($){

  function SketchPad(canvas) {
    this.canvas    = canvas;
    this.ctx       = canvas.getContext('2d');
    this.isDrawing = false;
    this.offset    = {
      left: canvas.offsetLeft,
      top:  canvas.offsetTop
    };
    this.prevX = this.prevY = this.currX = this.currY = 0;

    canvas.onmousedown = this.mousedown.bind(this);
    canvas.onmouseup   = this.mouseup.bind(this);
    canvas.onmousemove = this.mousemove.bind(this);
  }

  // calculate the canvas local postion
  SketchPad.prototype.calXY = function (e) {
    return {
      x: e.clientX - this.offset.left,
      y: e.clientY - this.offset.top
    };
  }

  SketchPad.prototype.mousedown = function (e) {
    var pos = this.calXY(e);
    this.prevX = pos.x;
    this.prevY = pos.y;
    this.isDrawing = true;
  }

  SketchPad.prototype.mouseup = function (e) {
    this.isDrawing = false;
  }

  SketchPad.prototype.mousemove = function (e) {
    if (!this.isDrawing) return;
    var pos = this.calXY(e);
    this.currX = pos.x;
    this.currY = pos.y;

    this.ctx.beginPath();
    this.ctx.moveTo(this.prevX, this.prevY);
    this.ctx.lineTo(this.currX, this.currY);
    this.ctx.strokeStyle = '#000';
    this.ctx.lineWidth = 2;
    this.ctx.stroke();
    this.ctx.closePath();

    this.prevX = this.currX;
    this.prevY = this.currY;
  }

  // plugin entrance
  $.fn.sketchpad = function() {
    this.css('border', '1px solid #000');

    // create sketchpads for every single element matched
    var sketchPads = [];
    this.each(function(index, el) {
      var canvasDom = $('<canvas></canvas>')[0];
      canvasDom.width = $(this).width();
      canvasDom.height = $(this).height();
      $(this).append(canvasDom);
      sketchPads[index] = new SketchPad(canvasDom);
    });

    // return array of sketchpad if matched multi elements
    return sketchPads.length === 1?sketchPads[0]:sketchPads;
  };
    
}(jQuery));
